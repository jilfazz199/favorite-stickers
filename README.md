# 我喜欢的表情包

我亲自挑选的表情包收藏。每张图片配有情绪、使用场景、画面描述和文字索引，方便 Claude 查找。

## 给 Claude 读

把这个文件夹交给 Claude，或在 Claude Code 中打开仓库目录，然后说：

> 这是我收藏的表情包。请先读 CLAUDE.md 和 index.json，再打开相关图片。按我当前的聊天内容，挑一张合适的，并告诉我文件路径。不要只读文件名就猜画面。

CLAUDE.md 是 Claude Code 的项目说明文件。普通 Claude 对话可上传需要的图片和索引。通过 API 使用时，需要由接入程序读取图片并作为图像输入传给模型；创建 Git 仓库或给出一个链接，不等于所有图片已进入模型上下文。

官方说明：[Claude Code 项目说明](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts)、[Claude 图像输入](https://platform.claude.com/docs/en/build-with-claude/vision)。

## 新增收藏

在这个仓库文件夹内执行：

```powershell
python tools/add_sticker.py 'D:/我的表情包/图片.jpg' --name '呼叫宝宝' --tags '撒娇,想你,呼唤' --text '呼叫宝宝 呼叫宝宝' --description '白色卡通角色，双手握在胸前，旁边飘着爱心。' --scene '亲昵地叫对方,想聊天'
git add .
git commit -m '添加喜欢的表情包'
```

导入脚本只使用 Python 标准库，不会访问网络或调用模型。它按文件内容去重，不修改原始图片。支持 JPG、PNG、GIF、WebP。

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
| 图片 | 名称 | 情绪 | 场景 |
| --- | --- | --- | --- |
| <img src="stickers/94545a96dad74636.jpg" width="140" alt="收藏表情"> | 呼叫宝宝 | 撒娇、想你、呼唤、可爱 | 亲昵地叫对方、想找对方聊天、表达想念 |
<!-- GALLERY:END -->

