<template>
  <div>
    <h2>Dashboard</h2>
    <el-row :gutter="16" style="margin-bottom:16px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-title">Models</div>
          <div class="stat-value">{{ modelsStore.models.length }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-title">Active Tasks</div>
          <div class="stat-value">{{ runningTasks }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-title">System</div>
          <el-tag :type="systemOk ? 'success' : 'danger'">
            {{ systemOk ? 'Online' : 'Offline' }}
          </el-tag>
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <template #header>Elo Leaderboard (All Dimensions)</template>
      <EloChart :entries="leaderboardStore.entries" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useModelsStore } from '../stores/models'
import { useTasksStore } from '../stores/tasks'
import { useLeaderboardStore } from '../stores/leaderboard'
import { systemApi } from '../api/system'
import EloChart from '../components/EloChart.vue'

const modelsStore = useModelsStore()
const tasksStore = useTasksStore()
const leaderboardStore = useLeaderboardStore()
const systemOk = ref(false)

const runningTasks = computed(() => tasksStore.tasks.filter((t) => t.status === 'running').length)

onMounted(async () => {
  await Promise.all([
    modelsStore.fetchModels(),
    tasksStore.fetchTasks(),
    leaderboardStore.fetch(),
  ])
  try {
    await systemApi.health()
    systemOk.value = true
  } catch {
    systemOk.value = false
  }
})
</script>

<style scoped>
.stat-title { font-size: 13px; color: #909399; margin-bottom: 8px; }
.stat-value { font-size: 28px; font-weight: bold; }
</style>
