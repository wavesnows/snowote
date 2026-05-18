<template>
  <div class="scheduler-panel">
    <div class="scheduler-header">
      <span class="scheduler-title">{{ t('scheduler.title') }}</span>
      <button class="settings-btn" @click="openManager" :title="t('taskManager.title')">⚙︎</button>
    </div>

    <div v-if="!allTasks.length" class="scheduler-empty">
      {{ t('scheduler.empty') }}
    </div>

    <div v-else class="task-list">
      <div
        v-for="item in allTasks"
        :key="item._key"
        class="task-row"
        @click="openManager"
      >
        <span class="status-dot" :class="item._dotClass" :title="item._dotTitle"></span>
        <div class="task-info">
          <span class="task-name">{{ item._label }}</span>
          <span class="task-meta">{{ item._meta }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import { ipcRenderer } from 'electron'
import { SchedulerTask } from '@/types/scheduler'
import { useTtsStore } from '@/store/store'
import { gitPull, gitHubPush } from '@/libs/github'

const { t } = useI18n()
const ttsStore = useTtsStore()

const internalTasks = ref<SchedulerTask[]>([])

type Row = { _key: string; _label: string; _meta: string; _dotClass: string; _dotTitle: string }

const allTasks = computed<Row[]>(() => {
  return internalTasks.value.map(task => ({
    _key: `int-${task.id}`,
    _label: task.name,
    _meta: task.lastRun ? relativeTime(task.lastRun) : t('scheduler.never'),
    _dotClass: dotClass(task),
    _dotTitle: dotTitle(task),
  }))
})

async function loadAll() {
  try {
    const internal = await ipcRenderer.invoke('scheduler:list')
    internalTasks.value = Array.isArray(internal) ? internal : []
  } catch (e) { console.error('scheduler:list error', e) }
}

function openManager() {
  ttsStore.config.taskManagerVisible = true
}

function dotClass(task: SchedulerTask): string {
  if (!task.enabled) return 'dot-grey'
  if (task.lastStatus === 'running') return 'dot-yellow'
  if (task.lastStatus === 'error') return 'dot-red'
  if (task.lastStatus === 'success') return 'dot-green'
  return 'dot-blue'
}

function dotTitle(task: SchedulerTask): string {
  if (!task.enabled) return t('scheduler.statusDisabled')
  return task.lastStatus
    ? t(`scheduler.status${task.lastStatus.charAt(0).toUpperCase() + task.lastStatus.slice(1)}`)
    : t('scheduler.never')
}

function relativeTime(ts: number): string {
  const diff = Date.now() - ts
  if (diff < 60000) return `${Math.floor(diff / 1000)}s ago`
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`
  return new Date(ts).toLocaleDateString()
}

function onTaskResult(_event: any, result: any) {
  const task = internalTasks.value.find(t => t.id === result.id)
  if (task) {
    task.lastStatus = result.status
    task.lastRun = result.timestamp
    task.lastError = result.error
  }
}

function onBuiltinAction(_event: any, action: string) {
  if (action === 'git-pull') {
    gitPull(t, ttsStore.notebook.currentPath).then((ok: boolean) => {
      ipcRenderer.send(`scheduler:builtin-result:git-pull`, { output: ok ? 'pulled' : '', error: ok ? undefined : 'pull failed' })
      if (ok) ttsStore.refreshTreeData()
    }).catch((e: any) => {
      ipcRenderer.send(`scheduler:builtin-result:git-pull`, { output: '', error: e.message })
    })
  } else if (action === 'git-push') {
    gitHubPush(t).then((ok: boolean) => {
      ipcRenderer.send(`scheduler:builtin-result:git-push`, { output: ok ? 'pushed' : '', error: ok ? undefined : 'push failed' })
    }).catch((e: any) => {
      ipcRenderer.send(`scheduler:builtin-result:git-push`, { output: '', error: e.message })
    })
  }
}

onMounted(() => {
  loadAll()
  ipcRenderer.on('task-result', onTaskResult)
  ipcRenderer.on('scheduler:builtin-action', onBuiltinAction)
  ipcRenderer.on('scheduler:refresh-tree', () => ttsStore.refreshTreeData())
  ipcRenderer.on('scheduler:tasks-changed', loadAll)
})

onBeforeUnmount(() => {
  ipcRenderer.removeListener('task-result', onTaskResult)
  ipcRenderer.removeListener('scheduler:builtin-action', onBuiltinAction)
  ipcRenderer.removeAllListeners('scheduler:refresh-tree')
  ipcRenderer.removeListener('scheduler:tasks-changed', loadAll)
})
</script>

<style scoped>
.scheduler-panel { display: flex; flex-direction: column; height: 100%; }
.scheduler-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 12px 6px; flex-shrink: 0;
}
.scheduler-title {
  font-size: 12px; font-weight: 600; color: #606266;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.settings-btn {
  width: 22px; height: 22px; border: none; background: transparent;
  cursor: pointer; font-size: 14px; color: #909399;
  display: flex; align-items: center; justify-content: center; border-radius: 4px;
}
.settings-btn:hover { background: rgba(0,0,0,0.06); color: #409eff; }
.scheduler-empty { padding: 16px 12px; font-size: 12px; color: #909399; text-align: center; }
.task-list { flex: 1; overflow-y: auto; }
.task-row {
  display: flex; align-items: center; gap: 8px;
  padding: 7px 10px; cursor: pointer;
  border-bottom: 1px solid rgba(0,0,0,0.04);
}
.task-row:hover { background: rgba(0,0,0,0.03); }
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-grey { background: #909399; }
.dot-green { background: #67c23a; }
.dot-red { background: #f56c6c; }
.dot-yellow { background: #e6a23c; }
.dot-blue { background: #409eff; }
.task-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.task-name { font-size: 12px; color: #303133; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.task-meta { font-size: 11px; color: #909399; }
</style>
