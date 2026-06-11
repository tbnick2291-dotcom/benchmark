<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>Models</h2>
      <el-button type="primary" @click="showCreateDialog = true">Register Model</el-button>
    </div>

    <el-table :data="modelsStore.models" v-loading="modelsStore.loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="model_path" label="Path" show-overflow-tooltip />
      <el-table-column prop="status" label="Status" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="180">
        <template #default="{ row }">
          <el-button
            v-if="row.status !== 'active'"
            size="small"
            type="success"
            @click="setStatus(row, 'active')"
          >Load</el-button>
          <el-button
            v-else
            size="small"
            type="warning"
            @click="setStatus(row, 'inactive')"
          >Unload</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showCreateDialog" title="Register Model" width="440px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="Name">
          <el-input v-model="form.name" placeholder="llama3-8b" />
        </el-form-item>
        <el-form-item label="Model Path">
          <el-input v-model="form.model_path" placeholder="/models/llama3-8b" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">Cancel</el-button>
        <el-button type="primary" :loading="creating" @click="submitCreate">Register</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useModelsStore } from '../stores/models'
import { ElMessage } from 'element-plus'

const modelsStore = useModelsStore()
const showCreateDialog = ref(false)
const creating = ref(false)
const form = ref({ name: '', model_path: '' })

onMounted(() => modelsStore.fetchModels())

async function submitCreate() {
  creating.value = true
  try {
    await modelsStore.createModel(form.value)
    showCreateDialog.value = false
    form.value = { name: '', model_path: '' }
    ElMessage.success('Model registered')
  } catch (e) {
    ElMessage.error(String(e))
  } finally {
    creating.value = false
  }
}

async function setStatus(row, status) {
  try {
    await modelsStore.updateStatus(row.id, status)
    ElMessage.success(`Model ${status === 'active' ? 'loaded' : 'unloaded'}`)
  } catch (e) {
    ElMessage.error(String(e))
  }
}
</script>
