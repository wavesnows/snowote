# Development Guide

## Prerequisites

- Node.js >= 14.17.0
- npm

## Setup

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

This runs `vite build && electron-builder` and outputs to `release/`.

## Project Structure

```
src/
  components/     Vue components
  store/          Pinia store
  i18n/           Translations (zh/en)
  libs/           Utility functions
  types/          TypeScript types
electron/
  main/           Main process
  preload/        Preload scripts
```

## Tech Stack

- Electron 24
- Vue 3 + TypeScript
- Vite
- Element Plus
- CodeMirror 6
- EditorJS
- simple-git
- node-cron
