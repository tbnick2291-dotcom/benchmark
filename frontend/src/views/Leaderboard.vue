<template>
  <div>
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px">
      <h2 style="margin:0">Leaderboard</h2>
      <el-select v-model="selectedDimension" placeholder="All Dimensions" clearable style="width:180px" @change="onDimChange">
        <el-option v-for="d in dimensions" :key="d" :value="d" :label="d" />
      </el-select>
    </div>

    <el-card style="margin-bottom:16px">
      <EloChart :entries="leaderboardStore.entries" />
    </el-card>

    <el-table :data="leaderboardStore.entries" v-loading="leaderboardStore.loading" stripe>
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="model_name" label="Model" />
      <el-table-column prop="dimension" label="Dimension" width="130" />
      <el-table-column prop="rating" label="Elo Rating" width="130" sortable>
        <template #default="{ row }">{{ row.rating.toFixed(1) }}</template>
      </el-table-column>
      <el-table-column prop="wins" label="W" width="60" />
      <el-table-column prop="losses" label="L" width="60" />
      <el-table-column prop="ties" label="T" width="60" />
      <el-table-column label="Win Rate" width="100">
        <template #default="{ row }">
          {{ ((row.wins / Math.max(row.wins + row.losses + row.ties, 1)) * 100).toFixed(1) }}%
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useLeaderboardStore } from '../stores/leaderboard'
import EloChart from '../components/EloChart.vue'

const leaderboardStore = useLeaderboardStore()
const selectedDimension = ref(null)
const dimensions = ['knowledge', 'reasoning', 'code', 'safety']

onMounted(() => leaderboardStore.fetch())

function onDimChange(val) {
  leaderboardStore.fetch(val || undefined)
}
</script>
