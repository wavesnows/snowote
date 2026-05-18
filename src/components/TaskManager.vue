<template>
  <el-dialog
    v-model="visible"
    :title="t('taskManager.title')"
    width="600px"
    top="6vh"
    :close-on-click-modal="true"
    :destroy-on-close="false"
    @open="onOpen"
  >
    <div class="tm-body" style="-webkit-app-region: no-drag">
      <div v-if="!tasks.length" class="tm-empty">{{ t('taskManager.noTasks') }}</div>
      <div v-else class="tm-list">
        <div v-for="task in tasks" :key="task.id" class="tm-row">
          <span class="tm-dot" :class="dotClass(task)" :title="dotTitle(task)"></span>
          <div class="tm-info">
            <div class="tm-name-row">
              <span class="tm-name">{{ task.name }}</span>
            </div>
            <div class="tm-meta">{{ scheduleDesc(task) }}</div>
          </div>
          <div class="tm-actions">
            <button class="tm-btn"
              :disabled="runningIds.has(task.id)"
              @click="runNow(task)"
              title="立即运行">
              {{ runningIds.has(task.id) ? '⏳' : '▶' }}
            </button>
            <button class="tm-btn tm-btn-danger" @click="removeTask(task)" title="删除">✕</button>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { ipcRenderer } from 'electron'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTtsStore } from '@/store/store'
import { SchedulerTask } from '@/types/scheduler'

const { t } = useI18n()
const ttsStore = useTtsStore()

const visible = computed({
  get: () => ttsStore.config.taskManagerVisible,
  set: (v) => { ttsStore.config.taskManagerVisible = v },
})

const tasks = ref<SchedulerTask[]>([])
const runningIds = ref(new Set<string>())

async function loadAll() {
  try {
    const result = await ipcRenderer.invoke('scheduler:list')
    tasks.value = Array.isArray(result) ? result : []
  } catch (e) { console.error('scheduler:list error', e) }
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

function scheduleDesc(task: SchedulerTask): string {
  const s = task.schedule
  if (s.mode === 'cron') return s.cron || ''
  const freq = s.frequency === 'daily' ? t('scheduler.daily') : s.frequency === 'weekly' ? t('scheduler.weekly') : t('scheduler.monthly')
  return `${freq} ${s.time || '09:00'}`
}

async function runNow(task: SchedulerTask) {
  const next = new Set(runningIds.value); next.add(task.id); runningIds.value = next
  try {
    await ipcRenderer.invoke('scheduler:run-now', { id: task.id })
    await loadAll()
  } finally {
    const after = new Set(runningIds.value); after.delete(task.id); runningIds.value = after
  }
}

async function removeTask(task: SchedulerTask) {
  try {
    await ElMessageBox.confirm(
      t('scheduler.confirmDelete', { name: task.name }),
      t('common.delete'),
      { confirmButtonText: t('common.ok'), cancelButtonText: t('common.cancel'), type: 'warning' }
    )
  } catch { return }
  await ipcRenderer.invoke('scheduler:delete', { id: task.id })
  ipcRenderer.send('scheduler:tasks-changed')
  await loadAll()
}

function onOpen() {
  loadAll()
}

watch(visible, (v) => { if (v) onOpen() })
ipcRenderer.on('scheduler:tasks-changed', loadAll)
</script>

<style scoped>
.tm-body { min-height: 200px; }
.tm-empty { padding: 24px; text-align: center; color: #909399; font-size: 13px; }
.tm-list { display: flex; flex-direction: column; gap: 2px; }
.tm-row {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 4px; border-bottom: 1px solid rgba(0,0,0,0.05);
}
.tm-row:last-child { border-bottom: none; }
.tm-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-grey { background: #909399; }
.dot-green { background: #67c23a; }
.dot-red { background: #f56c6c; }
.dot-yellow { background: #e6a23c; }
.dot-blue { background: #409eff; }
.tm-info { flex: 1; min-width: 0; }
.tm-name-row { display: flex; align-items: center; gap: 6px; }
.tm-name { font-size: 13px; color: #303133; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tm-meta { font-size: 11px; color: #909399; margin-top: 2px; }
.tm-actions { display: flex; gap: 4px; flex-shrink: 0; }
.tm-btn {
  width: 26px; height: 24px; border: none; background: transparent;
  cursor: pointer; font-size: 12px; color: #606266; border-radius: 3px;
  display: flex; align-items: center; justify-content: center;
}
.tm-btn:hover:not(:disabled) { background: rgba(0,0,0,0.07); color: #409eff; }
.tm-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.tm-btn-danger:hover:not(:disabled) { color: #f56c6c; }
</style>
