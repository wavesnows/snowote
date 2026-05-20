# snowote 使用与开发文档

[English](#quick-start) · [中文](#快速开始)

---

## Quick Start

1. Download the latest installer from [Releases](https://github.com/wavesnows/snowote/releases)
2. Install and open snowote
3. Open **Settings → Notebook**, choose a folder as your notes root directory
4. Start writing

## Features

- **Dual editor** — Rich text (EditorJS) or Markdown (CodeMirror), switch anytime
- **File tree** — Browse and organize notes as folders and files
- **Git sync** — Push/pull to GitHub or Gitee with one click
- **Version history** — Browse commit history, preview and restore any version
- **Full-text search** — Search across all notes instantly
- **Favorites** — Pin and star important notes
- **Terminal** — Built-in terminal panel, auto-opens to current note's directory
- **Scheduler** — Auto git-pull/push on a daily/weekly schedule

## Git Sync Setup

1. Open **Settings → Sync**
2. Select GitHub or Gitee
3. Enter your username and Personal Access Token (requires `repo` permission)
4. Add a remote notebook — snowote will clone an existing repo or create a new one
5. Use the toolbar git button to push/pull, or configure auto-sync in Scheduler

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+\`` | Toggle terminal |
| `Cmd/Ctrl+S` | Save note |
| `Cmd/Ctrl+Shift+P` | Git push |
| `Alt+↑/↓` | Navigate between notes |
| `Cmd/Ctrl+?` | Show help |

---

## 快速开始

1. 从 [Releases](https://github.com/wavesnows/snowote/releases) 下载最新安装包
2. 安装并打开 snowote
3. 打开**设置 → 笔记本**，选择一个文件夹作为笔记根目录
4. 开始写作

## 功能特性

- **双编辑器** — 富文本（EditorJS）或 Markdown（CodeMirror），随时切换
- **文件树** — 以文件夹和文件形式浏览和管理笔记
- **Git 同步** — 一键推送/拉取到 GitHub 或 Gitee
- **版本历史** — 浏览提交记录，预览并恢复任意版本
- **全文搜索** — 跨所有笔记即时搜索
- **收藏** — 置顶和星标重要笔记
- **内置终端** — 自动定位到当前笔记所在目录
- **调度器** — 按日/周自动 git-pull/push

## Git 同步配置

1. 打开**设置 → 同步**
2. 选择 GitHub 或 Gitee
3. 填写用户名和 Personal Access Token（需要 `repo` 权限）
4. 添加远程笔记本——snowote 会自动克隆已有仓库或新建仓库
5. 使用工具栏 git 按钮手动同步，或在调度器中配置自动同步

## 键盘快捷键

| 快捷键 | 操作 |
|---|---|
| `Ctrl+\`` | 切换终端 |
| `Cmd/Ctrl+S` | 保存笔记 |
| `Cmd/Ctrl+Shift+P` | Git 推送 |
| `Alt+↑/↓` | 切换笔记 |
| `Cmd/Ctrl+?` | 显示帮助 |

---

## Development

### Prerequisites

- Node.js >= 14.17.0
- npm

### Setup

```bash
npm install
npm run dev
```

### Build

```bash
npm run build
```

Outputs to `release/{version}/`.

### Tech Stack

- Electron 24 · Vue 3 · TypeScript · Vite
- Element Plus · CodeMirror 6 · EditorJS
- simple-git · node-cron · electron-updater
