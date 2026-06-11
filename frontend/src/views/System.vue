<template>
  <div>
    <h2>System Monitor</h2>
    <el-row :gutter="16">
      <el-col :span="12">
        <el-card>
          <template #header>vLLM Status</template>
          <p>Status: <el-tag :type="vllmStatus === 'online' ? 'success' : 'danger'">{{ vllmStatus }}</el-tag></p>
          <p>Loaded Models:</p>
          <el-tag v-for="m in loadedModels" :key="m" style="margin:4px">{{ m }}</el-tag>
          <el-empty v-if="loadedModels.length === 0" description="No models loaded" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>Health</template>
          <el-descriptions :column="1">
            <el-descriptions-item label="API">
              <el-tag :type="apiOk ? 'success' : 'danger'">{{ apiOk ? 'OK' : 'Error' }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
          <el-button style="margin-top:12px" @click="refresh">Refresh</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { systemApi } from '../api/system'

const vllmStatus = ref('unknown')
const loadedModels = ref([])
const apiOk = ref(false)

async function refresh() {
  try {
    await systemApi.health()
    apiOk.value = true
  } catch {
    apiOk.value = false
  }
  try {
    const status = await systemApi.status()
    vllmStatus.value = status.vllm_status
    loadedModels.value = status.loaded_models
  } catch {
    vllmStatus.value = 'offline'
    loadedModels.value = []
  }
}

onMounted(refresh)
</script>
