#!/usr/bin/env python3
"""Mirror four Emby icon indexes and their images into this repository."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import json
import os
import re
import sys
import time


SOURCES = (
    {"id": "lige", "file": "lige.json", "urls": ["https://raw.githubusercontent.com/lige47/QuanX-icon-rule/refs/heads/main/lige-emby-icon.json"]},
    {"id": "tfel", "file": "tfel.json", "urls": ["https://emby-icon.vercel.app/TFEL-Emby.json", "https://raw.githubusercontent.com/ztgetw/icon-proxy/icon/TFEL-Emby-Mirror.json"]},
    {"id": "baitang-yuan", "file": "baitang-yuan.json", "urls": ["https://raw.githubusercontent.com/baiitang/Sakura/main/Fileball/Yuan/tubiao.json"]},
    {"id": "baitang-fang", "file": "baitang-fang.json", "urls": ["https://raw.githubusercontent.com/baiitang/Sakura/main/Fileball/Fang/tubiao.json"]},
)
HEADERS = {"User-Agent": "Renly-Emby-Icons/1.0", "Accept": "*/*"}
MAX_IMAGE_BYTES = 6 * 1024 * 1024
MAX_INDEX_BYTES = 10 * 1024 * 1024
WORKERS = 8


def safe_url(value):
    """Encode non-ASCII paths without changing existing percent escapes."""
    parts = urlsplit(value)
    if parts.scheme not in ("http", "https") or not parts.netloc or parts.username or parts.password:
        raise ValueError("not a public HTTP(S) URL")
    return urlunsplit((parts.scheme, parts.netloc, quote(parts.path, safe="/%:@!$&'()*+,;=-._~"), parts.query, ""))


def read_url(url, max_bytes, headers=None):
    h = dict(HEADERS)
    h.update(headers or {})
    last = None
    for attempt in range(3):
        try:
            with urlopen(Request(safe_url(url), headers=h), timeout=25) as response:
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ValueError("response exceeds size limit")
                return data, dict(response.headers.items()), response.status
        except HTTPError as exc:
            if exc.code == 304:
                return b"", dict(exc.headers.items()), 304
            last = exc
            if exc.code not in (408, 429, 500, 502, 503, 504):
                break
        except (URLError, TimeoutError, OSError) as exc:
            last = exc
        if attempt < 2:
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(str(last))


def image_extension(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data.startswith(b"BM"):
        return ".bmp"
    if data.startswith(b"\x00\x00\x01\x00"):
        return ".ico"
    if b"<svg" in data[:4096].lower() and b"<html" not in data[:4096].lower():
        return ".svg"
    if len(data) >= 12 and data[4:12] in (b"ftypavif", b"ftypavis"):
        return ".avif"
    raise ValueError("response is not a recognized image")


def json_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def get_index(source):
    problems = []
    for url in source["urls"]:
        try:
            raw, _, _ = read_url(url, MAX_INDEX_BYTES)
            data = json.loads(raw.decode("utf-8-sig"))
            if not isinstance(data, dict) or not isinstance(data.get("icons"), list) or not data["icons"]:
                raise ValueError("index does not contain a non-empty icons list")
            return data, url, problems
        except (ValueError, UnicodeError, RuntimeError) as exc:
            problems.append({"url": url, "error": str(exc)})
    raise RuntimeError(json.dumps(problems, ensure_ascii=False))


def get_image(root, library, url, previous):
    # The TFEL fallback index wraps GitHub images in ghproxy.net. Fetch the
    # underlying raw image directly, without making our copy depend on it.
    actual = url
    if url.startswith("https://ghproxy.net/https://raw.githubusercontent.com/"):
        actual = url[len("https://ghproxy.net/"):]
    old_path = previous.get("path")
    old_file = root / old_path if old_path else None
    conditional = {}
    if old_file and old_file.is_file():
        if previous.get("etag"):
            conditional["If-None-Match"] = previous["etag"]
        if previous.get("last_modified"):
            conditional["If-Modified-Since"] = previous["last_modified"]
    raw, response_headers, status = read_url(actual, MAX_IMAGE_BYTES, conditional)
    if status == 304 and old_file and old_file.is_file():
        return old_path, previous
    ext = image_extension(raw)
    path = "images/" + library + "/" + sha256(url.encode("utf-8")).hexdigest() + ext
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or dest.read_bytes() != raw:
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        tmp.write_bytes(raw)
        tmp.replace(dest)
    headers = {k.lower(): v for k, v in response_headers.items()}
    return path, {"path": path, "etag": headers.get("etag"), "last_modified": headers.get("last-modified")}


def run(root=Path(".")):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or not re.fullmatch(r"[A-Za-z0-9_.-]+", branch):
        raise ValueError("GITHUB_REPOSITORY or GITHUB_REF_NAME is missing or invalid")
    raw_base = f"https://raw.githubusercontent.com/{repo}/{branch}/"
    cache_path = root / ".icon-cache.json"
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
        if not isinstance(cache, dict):
            cache = {}
    except (ValueError, OSError):
        cache = {}
    results = []
    has_failure = False
    for source in SOURCES:
        name = source["id"]
        print(f"Reading {name}...", flush=True)
        try:
            data, chosen_url, attempts = get_index(source)
        except RuntimeError as exc:
            results.append({"library": name, "status": "index_failed", "error": str(exc), "kept_previous": (root / source["file"]).exists()})
            has_failure = True
            print(f"{name}: index unavailable; previous index retained", flush=True)
            continue
        entries = data["icons"]
        jobs = {}
        errors = []
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            for index, item in enumerate(entries):
                if not isinstance(item, dict):
                    errors.append({"index": index, "error": "invalid icon entry"})
                    continue
                field = "url" if isinstance(item.get("url"), str) else "Url"
                url = item.get(field)
                if not isinstance(url, str):
                    errors.append({"index": index, "name": item.get("name"), "error": "missing URL"})
                    continue
                cache_key = name + "|" + url
                future = pool.submit(get_image, root, name, url, cache.get(cache_key, {}))
                jobs[future] = (index, field, url, cache_key)
            copied = 0
            for future in as_completed(jobs):
                index, field, url, cache_key = jobs[future]
                try:
                    path, metadata = future.result()
                    entries[index][field] = raw_base + path
                    cache[cache_key] = metadata
                    copied += 1
                    if copied % 100 == 0:
                        print(f"{name}: {copied}/{len(entries)} images", flush=True)
                except Exception as exc:
                    # Keep the original URL rather than silently introduce a broken link.
                    errors.append({"index": index, "name": entries[index].get("name"), "url": url, "error": str(exc)})
        json_write(root / source["file"], data)
        has_failure = has_failure or bool(errors)
        results.append({"library": name, "index": source["file"], "source_used": chosen_url, "fallback_source": chosen_url != source["urls"][0], "source_errors": attempts, "total": len(entries), "mirrored": copied, "original_urls_retained": len(errors), "errors": errors})
        print(f"{name}: {copied}/{len(entries)} mirrored, {len(errors)} failed", flush=True)
    json_write(cache_path, cache)
    json_write(root / "sync-status.json", {"updated_at_utc": datetime.now(timezone.utc).isoformat(), "libraries": results})
    return 1 if has_failure else 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception as exc:
        print(f"Sync error: {exc}", file=sys.stderr)
        sys.exit(1)
