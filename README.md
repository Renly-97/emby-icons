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

在 **Actions → 同步 Emby 图标 → Run workflow** 可以手动重新同步。修改同步程序后也会自动运行。本仓库没有设置定时更新。

- `sync-status.json` 记录每套清单的来源、图片总数和下载失败项。
- 若某套清单无法获取，会保留本仓库已有的清单。
- 若个别图片下载失败，清单中会暂时保留该图片的原始链接，并在状态文件中列出；成功下载的图片指向本仓库。
- GitHub Actions 每次运行的日志可在 Actions 页面查看。红色运行结果表示至少有一套来源或图片未完整同步。
