# 雪记（snowote）

一款轻量的本地优先笔记应用，基于 Electron + Vue 3 构建。支持 Markdown 和富文本编辑，Git 同步备份，版本历史浏览与恢复。

[下载](../../releases) · [使用说明](docs/user-guide.md) · [English](README.md)

---

## 功能特性

- **双编辑器** — Markdown（CodeMirror）或富文本（EditorJS），随时切换
- **Git 同步** — 一键推送/拉取到 GitHub 或 Gitee
- **版本历史** — 浏览 Git 提交记录，预览并恢复任意版本
- **全文搜索** — 跨所有笔记即时搜索
- **调度器** — 按日/周自动 git-pull/push
- **内置终端** — 快速终端面板（`Ctrl+\``）
- **收藏与最近** — 置顶、星标，快速访问常用笔记
- **中英双语** — 界面支持中文和英文切换

## 安装

从 [Releases](../../releases) 下载最新安装包：

- macOS：`snowote_x.x.x.dmg`
- Windows：`snowote_x.x.x.exe`

## 从源码构建

```bash
# 需要 Node.js >= 14.17.0
npm install
npm run dev      # 开发模式
npm run build    # 生产构建
```

## Git 同步配置

1. 打开 **设置 → 同步**
2. 选择 GitHub 或 Gitee
3. 填入用户名、仓库名和 Personal Access Token
4. 使用工具栏 Git 按钮手动同步，或在 **调度器** 中配置自动同步

## 捐赠

如果 snowote 对你有帮助，欢迎请我喝杯咖啡 ☕

<img src="src/assets/wx.jpg" width="180" alt="微信支付"> <img src="src/assets/zfb.jpg" width="180" alt="支付宝">

## 协议

MIT © [wavesnow](LICENSE)
