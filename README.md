# snowote（雪记）

A lightweight, local-first note-taking app built with Electron and Vue 3. Write in Markdown or rich text, sync with Git, and browse version history — all without leaving your desktop.

[Download](../../releases) · [User Guide](docs/user-guide.md) · [中文说明](README_CN.md)

---

## Features

- **Dual editor** — Markdown (CodeMirror) or rich text (EditorJS), switch anytime
- **Git sync** — Push/pull to GitHub or Gitee with one click
- **Version history** — Browse git commit history, preview and restore any version
- **Full-text search** — Search across all notes instantly
- **Scheduler** — Auto git-pull/push on a daily/weekly schedule
- **Built-in terminal** — Quick access terminal panel (`Ctrl+\``)
- **Favorites & Recent** — Pin, star, and quickly revisit notes
- **i18n** — English and Chinese UI

## Installation

Download the latest installer from [Releases](../../releases):

- macOS: `snowote_x.x.x.dmg`
- Windows: `snowote_x.x.x.exe`

## Build from Source

```bash
# Requires Node.js >= 14.17.0
npm install
npm run dev      # development
npm run build    # production build
```

## Git Sync Setup

1. Open **Settings → Sync**
2. Select GitHub or Gitee
3. Enter your username, repository name, and personal access token
4. Use the git button in the toolbar or configure auto-sync in **Scheduler**

See [User Guide](docs/user-guide.md) for details.

## Donate

If snowote is useful to you, consider buying me a coffee ☕

<img src="src/assets/wx.jpg" width="180" alt="WeChat Pay"> <img src="src/assets/zfb.jpg" width="180" alt="Alipay">

## License

MIT © [wavesnow](LICENSE)
