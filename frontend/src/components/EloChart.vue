<template>
  <v-chart :option="option" style="height:300px" autoresize />
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])

const props = defineProps({
  entries: { type: Array, default: () => [] },
})

const option = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: props.entries.map((e) => e.model_name) },
  yAxis: { type: 'value', name: 'Elo Rating', min: 1000 },
  series: [{ type: 'bar', data: props.entries.map((e) => e.rating), name: 'Elo' }],
}))
</script>
