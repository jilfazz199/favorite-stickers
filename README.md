# 我喜欢的表情包

我亲自挑选的表情包收藏。每张图片配有情绪、使用场景、画面描述和文字索引，方便 Claude 查找。

2026-10-27：目前9张已逐张看图标注，包括7张动图。`index.json` 包含实际画面、含义建议、适用/不适用场景。贴贴优先选“团子小熊贴贴”或“抱着转圈”，亲亲优先选“团子小熊亲亲”。

部分原始文件虽叫 `.jpg`，实际是 GIF。`stickers/` 保留用户原图，`previews/` 是按原始尺寸提取的 PNG 帧，`delivery/` 是与原文件字节相同、扩展名正确的发送副本。预览不重新绘图，不代表动图只有一帧。

## 给 Claude 读

把这个文件夹交给 Claude，或在 Claude Code 中打开仓库目录，然后说：

> 这是我收藏的表情包。请先读 CLAUDE.md 和 index.json，再打开相关图片。按我当前的聊天内容，挑一张合适的，并告诉我文件路径。不要只读文件名就猜画面。

如果 Claude 曾经克隆过本仓库，先让它在克隆目录执行 `git pull --ff-only`，再读更新后的说明和索引。已能使用文件工作区时，选图后可将 `delivery_path` 复制到输出目录并返回真实附件；是否显示内嵌预览由宿主界面决定。文件读取失败应说明具体工具错误。

CLAUDE.md 是 Claude Code 的项目说明文件。普通 Claude 对话可上传需要的图片和索引。通过 API 使用时，需要由接入程序读取图片并作为图像输入传给模型；创建 Git 仓库或给出一个链接，不等于所有图片已进入模型上下文。

官方说明：[Claude Code 项目说明](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts)、[Claude 图像输入](https://platform.claude.com/docs/en/build-with-claude/vision)。

## 新增收藏

在这个仓库文件夹内执行：

```powershell
python tools/add_sticker.py 'D:/我的表情包/图片.jpg' --name '呼叫宝宝' --tags '撒娇,想你,呼唤' --text '呼叫宝宝 呼叫宝宝' --description '白色卡通角色，双手握在胸前，旁边飘着爱心。' --scene '亲昵地叫对方,想聊天' --reviewed
git add .
git commit -m '添加喜欢的表情包'
```

导入和同步脚本需要 Python 与 Pillow（缺少时用 `python -m pip install Pillow` 安装）。脚本不访问网络或调用模型，不修改原始图片，支持 JPG、PNG、GIF、WebP。

直接在 GitHub 上传图片后，需要让 Claude 同步并补标注：

```text
先同步 favorite-stickers 的最新 main，在仓库目录运行 python tools/sync_index.py。
查看 review_status=pending 或 needs_review 的新图及其 PNG 预览，逐张补全画面、含义和场景。
实际看清后才标为 reviewed；不清楚的保持待确认，不凭文件名猜。
然后按 CLAUDE.md 选图，发图时使用 delivery_path。
```

`sync_index.py` 只登记新图、生成预览和检测变化，不会自动理解表情。新文件默认待标注，旧文件被替换后重新待核对。`python tools/sync_index.py --check` 可检查索引覆盖、预览和发送副本是否与原图一致。

## 上传 GitHub

本地 Git 仓库与 GitHub 上的远程仓库是两件事。远程仓库的可见性由你选择；私有仓库需给使用它的工具授予访问权限。

在 GitHub 新建空仓库后，可在此目录执行以下命令。先把占位地址改成自己的仓库地址：

```powershell
git remote add origin https://github.com/YOUR_ACCOUNT/favorite-stickers.git
git push -u origin main
```

## 素材来源

图片由用户提供并收藏，具体作者与授权情况在索引中记录。仓库不对来源不明的图片另行授予开源许可证。

## 图册

<!-- GALLERY:START -->
| 图片 | 名称 | 情绪 | 场景 | 标注状态 |
| --- | --- | --- | --- | --- |
| <img src="previews/ce3b658ad22f1e82/frame-000.png" width="140" alt="收藏表情"> | 抱枕困困 | 困困、晚安、睡觉、休息 | 说晚安、表达困倦、准备休息 | 已看图标注 |
| <img src="previews/1f44d8fe6e81b0fa/frame-000.png" width="140" alt="收藏表情"> | 团子吃饭 | 吃饭、干饭、吃东西、食物 | 说要去吃饭、聊食物、表达正在吃东西 | 已看图标注 |
| <img src="previews/0bd4020d1cda4bd1/frame-000.png" width="140" alt="收藏表情"> | 黑猫探头盯着看 | 黑猫、探头、盯着看、疑惑 | 好奇围观、探头看看、等对方说话 | 已看图标注 |
| <img src="previews/94545a96dad74636/frame-000.png" width="140" alt="收藏表情"> | 呼叫宝宝 | 撒娇、想你、呼唤、可爱 | 亲昵地叫对方、想找对方聊天、表达想念 | 已看图标注 |
| <img src="previews/faa638a8bc2ab5e2/frame-000.png" width="140" alt="收藏表情"> | 团子小熊贴贴 | 贴贴、抱抱、拥抱、依偎、亲昵 | 回应贴贴、想抱抱、亲昵地陪伴 | 已看图标注 |
| <img src="previews/56175baefe3842d8/frame-000.png" width="140" alt="收藏表情"> | 抱着转圈 | 贴贴、抱抱、拥抱、转圈、开心 | 回应抱抱、开心贴贴、表达见面的喜悦 | 已看图标注 |
| <img src="previews/d2de449a4f80c913/frame-000.png" width="140" alt="收藏表情"> | 爱心黑猫探头 | 黑猫、爱心、探头、喜欢 | 表达喜欢、可爱地露个头、表示在关注对方 | 已看图标注 |
| <img src="previews/f476d98b3f15cb25/frame-000.png" width="140" alt="收藏表情"> | 团子小熊亲亲 | 亲亲、亲吻、亲昵、贴贴 | 回应亲亲、想亲一下、亲昵地贴近 | 已看图标注 |
| <img src="previews/f57001780b335a08/frame-000.png" width="140" alt="收藏表情"> | 头顶长花花 | 长花花、小花、可爱、卖萌 | 轻松卖萌、聊花或表达好心情 | 已看图标注 |
<!-- GALLERY:END -->

