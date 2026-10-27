# Renly 的 Emby 图标库

四套图标清单分别保存，清单和成功下载的图片由本仓库提供。各图标的作者和原始来源见下方。

## 图标库地址

首次同步成功后，可以在支持图标库的客户端中填入：

| 图标库 | 清单地址 |
| --- | --- |
| 离歌 Emby | https://raw.githubusercontent.com/Renly-97/emby-icons/main/lige.json |
| TFEL | https://raw.githubusercontent.com/Renly-97/emby-icons/main/tfel.json |
| 白糖圆形 | https://raw.githubusercontent.com/Renly-97/emby-icons/main/baitang-yuan.json |
| 白糖方形 | https://raw.githubusercontent.com/Renly-97/emby-icons/main/baitang-fang.json |

## 来源与致谢

- 离歌：<https://github.com/lige47/lige_icon>。作者请求不要 Fork，引用或转载需注明出处。
- TFEL：<https://emby-icon.vercel.app/TFEL-Emby.json>。原始地址不可用时，程序会尝试使用 [ztgetw/icon-proxy](https://github.com/ztgetw/icon-proxy) 提供的镜像，并在状态文件中标明。
- 白糖圆形和方形：<https://github.com/baiitang/Sakura>。图标库也引用了 [Softlyx/Fileball](https://github.com/Softlyx/Fileball) 等作者的图片，感谢原作者。
- 白糖仓库说明请勿直接 Fork；转载研究须保留作者署名，并写有下载后 24 小时删除及禁止在中华人民共和国境内平台公开传播或牟利的要求。使用时请参阅原作者说明。

## 更新和检查

每周一北京时间 04:17 自动同步四套图标（GitHub 排队时可能延迟）。也可以在 **Actions → 同步 Emby 图标 → Run workflow** 手动同步。修改同步程序后也会自动运行。

- `sync-status.json` 记录每套清单的来源、图片总数和下载失败项。
- 若某套清单无法获取，会保留本仓库已有的清单。
- 若图片临时下载失败，已有备份会继续使用本仓库中的图片；没有备份时暂时保留原始链接。失败项都会记录在状态文件中。
- GitHub Actions 每次运行的日志可在 Actions 页面查看。红色运行结果表示至少有一套来源或图片未完整同步。

## 已知上游缺失（2026-10-27 检查）

- TFEL 的 `Juhaokan_1` 图片在原站返回 404，本仓库保留原链接并在状态文件中报告；原站修复后可重新同步。其余图标图片均已保存。
