<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <div class="welcome-header">
        <div class="logo">
          <el-icon :size="80" color="#409eff"><Document /></el-icon>
        </div>
        <h1>{{ t('welcome.title') }}</h1>
        <p class="subtitle">{{ t('welcome.subtitle') }}</p>
      </div>

      <div class="welcome-body">
        <!-- 左列：2×2 快捷操作 -->
        <div class="left-column">
          <h3 class="section-title">{{ t('welcome.quickActions') }}</h3>
          <div class="quick-actions">
            <div class="action-card" @click="createNote">
              <el-icon :size="32" color="#67c23a"><DocumentAdd /></el-icon>
              <h3>{{ t('welcome.createNote') }}</h3>
              <p>{{ t('welcome.createNoteDesc') }}</p>
            </div>
            <div class="action-card" @click="openSettings">
              <el-icon :size="32" color="#e6a23c"><Setting /></el-icon>
              <h3>{{ t('welcome.settings') }}</h3>
              <p>{{ t('welcome.settingsDesc') }}</p>
            </div>
            <div class="action-card" @click="showHelp">
              <el-icon :size="32" color="#909399"><QuestionFilled /></el-icon>
              <h3>{{ t('welcome.help') }}</h3>
              <p>{{ t('welcome.helpDesc') }}</p>
            </div>
            <div class="action-card" @click="showDonate = true">
              <span class="coffee-icon">☕</span>
              <h3>{{ t('welcome.donate') }}</h3>
              <p>{{ t('welcome.donateDesc') }}</p>
            </div>
          </div>
        </div>

        <!-- 右列：提示 + 关于 -->
        <div class="right-column">
          <div class="tips">
            <h3>{{ t('welcome.tipsTitle') }}</h3>
            <ul>
              <li>{{ t('welcome.tip1') }}</li>
              <li>{{ t('welcome.tip2') }}</li>
              <li>{{ t('welcome.tip3') }}</li>
            </ul>
          </div>

          <div class="about-card">
            <div class="about-card-header">
              <el-icon :size="28" color="#409eff"><Document /></el-icon>
              <div>
                <div class="about-card-name">snowote <span class="about-card-cn">雪记</span></div>
                <div class="about-card-version">v{{ appVersion }}</div>
              </div>
            </div>
            <p class="about-card-desc">{{ t('help.aboutDesc') }}</p>
            <div class="about-card-actions">
              <button class="about-btn-coffee" @click="showDonate = true">{{ t('help.aboutDonate') }}</button>
            </div>
          </div>
        </div>
      </div>

      <div class="welcome-footer">
        <span>{{ t('welcome.footerText') }}</span>
        <button class="github-link" @click="openGithub">{{ t('welcome.footerStar') }}</button>
      </div>
    </div>

    <!-- 捐助弹窗 -->
    <el-dialog
      v-model="showDonate"
      :title="t('welcome.donateTitle')"
      width="420px"
      align-center
    >
      <div class="donate-dialog">
        <p class="donate-desc">{{ t('welcome.donateDialogDesc') }}</p>
        <div class="donate-qr">
          <div class="qr-item">
            <img src="../../assets/wx.jpg" alt="WeChat Pay" />
            <span>{{ t('help.aboutDonateWechat') }}</span>
          </div>
          <div class="qr-item">
            <img src="../../assets/zfb.jpg" alt="Alipay" />
            <span>{{ t('help.aboutDonateAlipay') }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Document, DocumentAdd, Setting, QuestionFilled } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'
import { useTtsStore } from '@/store/store'

const { t } = useI18n()
const ttsStore = useTtsStore()
const showDonate = ref(false)

const createNote = async () => {
  const fs = await import('fs')
  const path = await import('path')

  const notebookPath = ttsStore.notebook.currentPath
  if (!fs.existsSync(notebookPath)) {
    try {
      fs.mkdirSync(notebookPath, { recursive: true })
    } catch (error) {
      console.error('Failed to create notebook directory:', error)
      return
    }
  }

  if (ttsStore.treeMenu.data.length === 0) {
    const folderPath = path.join(notebookPath, 'notes')
    try {
      fs.mkdirSync(folderPath, { recursive: true })
      ttsStore.refreshTreeData()
      await new Promise(resolve => setTimeout(resolve, 200))
    } catch (error) {
      console.error('Failed to create folder:', error)
      return
    }
  }

  const treeData = ttsStore.treeMenu.data
  if (treeData.length === 0) return

  const notePath = path.join(treeData[0].path, 'Welcome.json')
  const emptyEditorData = {
    time: Date.now(),
    blocks: [
      { type: "header", data: { text: "Welcome to snowote 👋", level: 1 } },
      { type: "paragraph", data: { text: "Start writing your notes here." } }
    ],
    version: "2.26.5"
  }

  try {
    fs.writeFileSync(notePath, JSON.stringify(emptyEditorData, null, 2), 'utf8')
    ttsStore.refreshTreeData()
    await new Promise(resolve => setTimeout(resolve, 200))
    ttsStore.inputs.notePath = notePath
    ttsStore.cnote.title = 'Welcome'
    ttsStore.cnote.destTitle = 'Welcome'
    ttsStore.cnote.lastPath = notePath
    ttsStore.editerData = emptyEditorData
    ttsStore.setLastEditNote()
  } catch (error) {
    console.error('Failed to create note:', error)
  }
}

const openSettings = () => { ttsStore.config.drawer = true }
const showHelp = () => { ttsStore.openHelpDialog() }

const { shell, ipcRenderer } = require('electron')
const appVersion = ref('')
onMounted(async () => {
  appVersion.value = await ipcRenderer.invoke('app:version')
})

function openGithub() {
  shell.openExternal('https://github.com/wavesnows/snowote')
}
</script>

<style scoped>
.welcome-container {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
}

.welcome-content {
  max-width: 1200px;
  width: 100%;
}

.welcome-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo { margin-bottom: 20px; }

h1 {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 10px 0;
}

.subtitle {
  font-size: 16px;
  color: #606266;
  margin: 0;
}

.welcome-body {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 900px) {
  .welcome-body { grid-template-columns: 1fr 1fr; }
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
  text-align: center;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
}

/* 2×2 网格 */
.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.action-card {
  background: white;
  padding: 20px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.action-card h3 {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.action-card p {
  font-size: 12px;
  color: #909399;
  margin: 0;
  line-height: 1.5;
}

.coffee-icon {
  font-size: 32px;
  line-height: 1;
}

/* 右列 */
.tips {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tips h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
}

.tips ul {
  margin: 0;
  padding-left: 24px;
}

.tips li {
  font-size: 14px;
  color: #606266;
  line-height: 2;
  margin-bottom: 12px;
}

.tips li:last-child { margin-bottom: 0; }

.about-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 16px;
}

.about-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.about-card-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.about-card-cn {
  font-size: 13px;
  color: #909399;
  font-weight: 400;
  margin-left: 4px;
}

.about-card-version {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.about-card-desc {
  font-size: 13px;
  color: #606266;
  margin: 0 0 14px;
  line-height: 1.6;
}

.about-card-actions {
  display: flex;
  gap: 8px;
}

.about-btn-coffee {
  border-radius: 16px;
  padding: 4px 14px;
  font-size: 12px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  background: #fff0f0;
  border: 1px solid #ffb8b8;
  color: #c0392b;
}

.about-btn-coffee:hover {
  background: #ffe4e4;
  border-color: #ff7875;
}

/* 底部 */
.welcome-footer {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  text-align: center;
  font-size: 13px;
  color: #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.github-link {
  background: #fffbe6;
  border: 1px solid #ffd666;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 13px;
  color: #d48806;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.github-link:hover {
  background: #fff1b8;
  border-color: #faad14;
  color: #ad6800;
}

/* 捐助弹窗 */
.donate-dialog {
  text-align: center;
}

.donate-desc {
  font-size: 14px;
  color: #606266;
  margin: 0 0 24px;
}

.donate-qr {
  display: flex;
  justify-content: center;
  gap: 32px;
}

.qr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.qr-item img {
  width: 150px;
  height: 150px;
  border-radius: 8px;
  object-fit: cover;
}

.qr-item span {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
}

@media (max-width: 899px) {
  .section-title { text-align: left; }
}
</style>
