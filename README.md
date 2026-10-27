# Renly 的 Emby 图标库

> 本仓库仅用于个人学习、研究、备份和自用，不作商业用途，也不主动向他人分享或推广。感谢各位原作者制作和整理图标，图标相关权利归各自作者所有。
>
> 仓库目前为公开状态，方便本人在图标客户端读取；

## 原作者和原始地址

| 图标库 | 原作者 | 原始图标库 |
| --- | --- | --- |
| 离歌 Emby | [lige47 / 离歌](https://github.com/lige47/lige_icon) | https://raw.githubusercontent.com/lige47/QuanX-icon-rule/refs/heads/main/lige-emby-icon.json |
| TFEL | TFEL | https://emby-icon.vercel.app/TFEL-Emby.json |
| 白糖圆形 | [baiitang / 白糖](https://github.com/baiitang/Sakura) | https://raw.githubusercontent.com/baiitang/Sakura/main/Fileball/Yuan/tubiao.json |
| 白糖方形 | [baiitang / 白糖](https://github.com/baiitang/Sakura) | https://raw.githubusercontent.com/baiitang/Sakura/main/Fileball/Fang/tubiao.json |

白糖图标库在 [Softlyx/Fileball](https://github.com/Softlyx/Fileball) 等作者的图标基础上整理，也感谢相关原作者。TFEL 原始地址不可用时，程序会尝试 [ztgetw/icon-proxy](https://github.com/ztgetw/icon-proxy) 的镜像，并在状态文件中标明。


## 本仓库的图标库地址

| 图标库 | 清单地址 |
| --- | --- |
| 离歌 Emby | https://raw.githubusercontent.com/Renly-97/emby-icons/main/lige.json |
| TFEL | https://raw.githubusercontent.com/Renly-97/emby-icons/main/tfel.json |
| 白糖圆形 | https://raw.githubusercontent.com/Renly-97/emby-icons/main/baitang-yuan.json |
| 白糖方形 | https://raw.githubusercontent.com/Renly-97/emby-icons/main/baitang-fang.json |

## 更新和备份

每周一北京时间 04:17 自动同步四套图标（GitHub 排队时可能延迟）。也可以在 **Actions → 同步 Emby 图标 → Run workflow** 手动同步。

- 原始图标库地址失效或清单获取失败时，保留已有清单和图片；程序不能自动猜出新的图标库地址。
- 图片地址变动后，如果新地址不可用，会优先保留本仓库已有的对应图片；无法安全辨认的同名图片会保留旧条目，避免错误匹配。
- 原图标库移除条目时，会保留本仓库已有且可用的旧图标条目。同一地址的图片内容发生变化时，旧图片文件也会保留。
- `sync-status.json` 记录来源、同步数量、保留的旧条目和失败项。红色运行结果表示至少一套来源或图片未完整同步。

## 已知上游缺失（2026-10-27 检查）

TFEL 的 `Juhaokan_1` 图片在原站返回 404，本仓库没有该图片的备份，暂时保留原链接并在状态文件中报告；原站修复后可重新同步。
