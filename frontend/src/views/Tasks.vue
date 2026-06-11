<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>Evaluation Tasks</h2>
      <el-button type="primary" @click="showDialog = true">New Task</el-button>
    </div>

    <el-table :data="tasksStore.tasks" v-loading="tasksStore.loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="dimension" label="Dimension" width="120" />
      <el-table-column prop="status" label="Status" width="120">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="Created" width="180">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleString() }}</template>
      </el-table-column>
      <el-table-column label="Actions" width="120">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending'"
            size="small"
            type="primary"
            @click="startTask(row.id)"
          >Start</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" title="Create Task" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Dimension">
          <el-select v-model="form.dimension" style="width:100%">
            <el-option v-for="d in dimensions" :key="d" :value="d" :label="d" />
          </el-select>
        </el-form-item>
        <el-form-item label="Models">
          <el-select v-model="form.model_ids" multiple style="width:100%">
            <el-option
              v-for="m in modelsStore.models"
              :key="m.id"
              :value="m.id"
              :label="m.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Rounds">
          <el-input-number v-model="form.rounds" :min="1" :max="20" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">Cancel</el-button>
        <el-button type="primary" @click="submitCreate">Create</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTasksStore } from '../stores/tasks'
import { useModelsStore } from '../stores/models'
import { ElMessage } from 'element-plus'

const tasksStore = useTasksStore()
const modelsStore = useModelsStore()
const showDialog = ref(false)
const dimensions = ['knowledge', 'reasoning', 'code', 'safety']
const form = ref({ name: '', dimension: 'knowledge', model_ids: [], rounds: 3 })

onMounted(async () => {
  await Promise.all([tasksStore.fetchTasks(), modelsStore.fetchModels()])
})

function statusType(status) {
  return { pending: 'info', running: 'warning', completed: 'success', failed: 'danger' }[status] ?? 'info'
}

async function startTask(id) {
  try {
    await tasksStore.startTask(id)
    ElMessage.success('Task started')
  } catch (e) {
    ElMessage.error(String(e))
  }
}

async function submitCreate() {
  try {
    await tasksStore.createTask({
      name: form.value.name,
      dimension: form.value.dimension,
      task_type: 'adversarial',
      config: { model_ids: form.value.model_ids, rounds: form.value.rounds },
    })
    showDialog.value = false
    ElMessage.success('Task created')
  } catch (e) {
    ElMessage.error(String(e))
  }
}
</script>
