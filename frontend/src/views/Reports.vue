<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>Reports</h2>
      <el-button type="primary" @click="showDialog = true">Generate Report</el-button>
    </div>

    <el-table :data="reports" v-loading="loading" stripe @row-click="openReport">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="model_id" label="Model ID" width="100" />
      <el-table-column prop="report_type" label="Type" width="100" />
      <el-table-column prop="generated_at" label="Generated" width="180">
        <template #default="{ row }">{{ new Date(row.generated_at).toLocaleString() }}</template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" title="Generate Report" width="440px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Model">
          <el-select v-model="form.model_id" style="width:100%">
            <el-option v-for="m in modelsStore.models" :key="m.id" :value="m.id" :label="m.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="Type">
          <el-select v-model="form.report_type" style="width:100%">
            <el-option value="full" label="Full" />
            <el-option value="summary" label="Summary" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">Cancel</el-button>
        <el-button type="primary" :loading="generating" @click="generate">Generate</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showReportDetail" title="Report Detail" width="700px">
      <pre style="max-height:500px;overflow:auto;white-space:pre-wrap">{{ JSON.stringify(selectedReport?.content, null, 2) }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { reportsApi } from '../api/reports'
import { useModelsStore } from '../stores/models'
import { ElMessage } from 'element-plus'

const modelsStore = useModelsStore()
const reports = ref([])
const loading = ref(false)
const showDialog = ref(false)
const generating = ref(false)
const showReportDetail = ref(false)
const selectedReport = ref(null)
const form = ref({ model_id: null, report_type: 'full' })

onMounted(async () => {
  await modelsStore.fetchModels()
  loading.value = true
  try {
    reports.value = await reportsApi.list()
  } finally {
    loading.value = false
  }
})

async function generate() {
  generating.value = true
  try {
    const report = await reportsApi.generate({ model_id: form.value.model_id, task_ids: [], report_type: form.value.report_type })
    reports.value.unshift(report)
    showDialog.value = false
    ElMessage.success('Report generated')
  } catch (e) {
    ElMessage.error(String(e))
  } finally {
    generating.value = false
  }
}

function openReport(row) {
  selectedReport.value = row
  showReportDetail.value = true
}
</script>
