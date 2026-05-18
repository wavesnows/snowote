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
        <div v-for="task in tasks" :key="task.id" class="tm-row-wrap">
          <!-- 任务行 -->
          <div class="tm-row">
            <el-switch
              :model-value="task.enabled"
              size="small"
              @change="(v: boolean) => toggleEnabled(task, v)"
            />
            <span class="tm-dot" :class="dotClass(task)" :title="dotTitle(task)"></span>
            <div class="tm-info">
              <div class="tm-name">{{ task.name }}</div>
              <div class="tm-meta">{{ scheduleDesc(task) }}</div>
            </div>
            <div class="tm-actions">
              <button class="tm-btn"
                :disabled="runningIds.has(task.id)"
                @click="runNow(task)"
                :title="t('scheduler.runNow')">
                {{ runningIds.has(task.id) ? '⏳' : '▶' }}
              </button>
              <button class="tm-btn" @click="toggleEdit(task.id)" :title="t('scheduler.editTask')">✎</button>
              <button class="tm-btn tm-btn-danger" @click="removeTask(task)" :title="t('scheduler.delete')">✕</button>
            </div>
          </div>

          <!-- 内联编辑表单 -->
          <div v-if="editingId === task.id" class="tm-edit-form">
            <el-form :model="editForm" label-position="top" size="small">
              <el-form-item :label="t('scheduler.taskName')">
                <el-input v-model="editForm.name" :placeholder="t('scheduler.taskNamePlaceholder')" />
              </el-form-item>

              <el-form-item :label="t('scheduler.action')">
                <el-select v-model="editForm.action" style="width:100%">
                  <el-option value="git-pull" :label="t('scheduler.gitPull')" />
                  <el-option value="git-push" :label="t('scheduler.gitPush')" />
                  <el-option value="refresh-tree" :label="t('scheduler.refreshTree')" />
                </el-select>
              </el-form-item>

              <el-form-item :label="t('scheduler.schedule')">
                <el-radio-group v-model="editForm.scheduleMode" size="small">
                  <el-radio-button value="simple">{{ t('scheduler.simple') }}</el-radio-button>
                  <el-radio-button value="cron">{{ t('scheduler.cron') }}</el-radio-button>
                </el-radio-group>
              </el-form-item>

              <template v-if="editForm.scheduleMode === 'simple'">
                <el-form-item :label="t('scheduler.frequency')">
                  <el-select v-model="editForm.frequency" style="width:100%">
                    <el-option value="daily" :label="t('scheduler.daily')" />
                    <el-option value="weekly" :label="t('scheduler.weekly')" />
                    <el-option value="monthly" :label="t('scheduler.monthly')" />
                  </el-select>
                </el-form-item>
                <el-form-item :label="t('scheduler.time')">
                  <el-input v-model="editForm.time" placeholder="09:00" style="width:120px" />
                </el-form-item>
                <el-form-item v-if="editForm.frequency === 'weekly'" :label="t('scheduler.weekday')">
                  <el-select v-model="editForm.weekday" style="width:100%">
                    <el-option :value="1" label="周一" />
                    <el-option :value="2" label="周二" />
                    <el-option :value="3" label="周三" />
                    <el-option :value="4" label="周四" />
                    <el-option :value="5" label="周五" />
                    <el-option :value="6" label="周六" />
                    <el-option :value="0" label="周日" />
                  </el-select>
                </el-form-item>
                <el-form-item v-if="editForm.frequency === 'monthly'" :label="t('scheduler.dayOfMonth')">
                  <el-input-number v-model="editForm.day" :min="1" :max="28" style="width:120px" />
                </el-form-item>
              </template>

              <el-form-item v-else :label="t('scheduler.cronExpression')">
                <el-input v-model="editForm.cron" placeholder="0 9 * * *" />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" size="small" @click="saveEdit(task)">{{ t('common.save') }}</el-button>
                <el-button size="small" @click="editingId = null">{{ t('common.cancel') }}</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, computed, reactive, watch, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import { ipcRenderer } from 'electron'
import { ElMessageBox } from 'element-plus'
import { useTtsStore } from '@/store/store'
import { SchedulerTask, simpleToCron } from '@/types/scheduler'

const { t } = useI18n()
const ttsStore = useTtsStore()

const visible = computed({
  get: () => ttsStore.config.taskManagerVisible,
  set: (v) => { ttsStore.config.taskManagerVisible = v },
})

const tasks = ref<SchedulerTask[]>([])
const runningIds = ref(new Set<string>())
const editingId = ref<string | null>(null)

const editForm = reactive({
  name: '',
  action: 'git-pull' as 'git-pull' | 'git-push' | 'refresh-tree',
  scheduleMode: 'simple' as 'simple' | 'cron',
  frequency: 'daily' as 'daily' | 'weekly' | 'monthly',
  time: '09:00',
  weekday: 1,
  day: 1,
  cron: '0 9 * * *',
})

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

function toggleEdit(id: string) {
  if (editingId.value === id) {
    editingId.value = null
    return
  }
  const task = tasks.value.find(t => t.id === id)
  if (!task) return
  editForm.name = task.name
  editForm.action = task.action || 'git-pull'
  editForm.scheduleMode = task.schedule.mode
  editForm.frequency = task.schedule.frequency || 'daily'
  editForm.time = task.schedule.time || '09:00'
  editForm.weekday = task.schedule.weekday ?? 1
  editForm.day = task.schedule.day ?? 1
  editForm.cron = task.schedule.cron || '0 9 * * *'
  editingId.value = id
}

async function toggleEnabled(task: SchedulerTask, enabled: boolean) {
  const updated = { ...task, enabled }
  await ipcRenderer.invoke('scheduler:save', updated)
  await loadAll()
}

async function saveEdit(task: SchedulerTask) {
  const updated: SchedulerTask = {
    ...task,
    name: editForm.name,
    action: editForm.action,
    schedule: editForm.scheduleMode === 'cron'
      ? { mode: 'cron', cron: editForm.cron }
      : {
          mode: 'simple',
          frequency: editForm.frequency,
          time: editForm.time,
          weekday: editForm.weekday,
          day: editForm.day,
          cron: simpleToCron({ ...task, schedule: { mode: 'simple', frequency: editForm.frequency, time: editForm.time, weekday: editForm.weekday, day: editForm.day } }),
        },
  }
  await ipcRenderer.invoke('scheduler:save', updated)
  editingId.value = null
  await loadAll()
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
  editingId.value = null
  loadAll()
}

watch(visible, (v) => { if (v) onOpen() })

onMounted(() => {
  ipcRenderer.on('scheduler:tasks-changed', loadAll)
})

onBeforeUnmount(() => {
  ipcRenderer.removeListener('scheduler:tasks-changed', loadAll)
})
</script>

<style scoped>
.tm-body { min-height: 200px; }
.tm-empty { padding: 24px; text-align: center; color: #909399; font-size: 13px; }
.tm-list { display: flex; flex-direction: column; gap: 2px; }
.tm-row-wrap { border-bottom: 1px solid rgba(0,0,0,0.05); }
.tm-row-wrap:last-child { border-bottom: none; }
.tm-row {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 4px;
}
.tm-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-grey { background: #909399; }
.dot-green { background: #67c23a; }
.dot-red { background: #f56c6c; }
.dot-yellow { background: #e6a23c; }
.dot-blue { background: #409eff; }
.tm-info { flex: 1; min-width: 0; }
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
.tm-edit-form {
  padding: 12px 12px 4px;
  background: rgba(0,0,0,0.02);
  border-top: 1px solid rgba(0,0,0,0.05);
}
</style>
