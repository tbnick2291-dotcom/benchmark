<template>
  <div>
    <el-page-header @back="$router.back()" title="Battles" :content="`Battle #${route.params.id}`" />
    <div style="margin-top:16px" v-loading="loading">
      <template v-if="battle">
        <el-card style="margin-bottom:12px">
          <template #header>Question</template>
          <pre style="white-space:pre-wrap">{{ question?.content ?? '(loading)' }}</pre>
        </el-card>

        <el-row :gutter="16">
          <el-col :span="12">
            <el-card>
              <template #header>
                Attacker (Model #{{ battle.attacker_id }})
                <el-tag type="warning" style="margin-left:8px">Attacker</el-tag>
              </template>
              <pre style="white-space:pre-wrap">{{ battle.attacker_answer }}</pre>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                Defender (Model #{{ battle.defender_id }})
                <el-tag type="info" style="margin-left:8px">Defender</el-tag>
              </template>
              <pre style="white-space:pre-wrap">{{ battle.defender_answer }}</pre>
            </el-card>
          </el-col>
        </el-row>

        <el-card style="margin-top:12px">
          <template #header>
            Verdict
            <el-tag
              :type="battle.winner === 'attacker' ? 'danger' : battle.winner === 'defender' ? 'success' : 'warning'"
              style="margin-left:8px"
            >{{ battle.winner }}</el-tag>
          </template>
          <p>{{ battle.judge_reason }}</p>
        </el-card>
      </template>
      <el-empty v-else description="Battle not found" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { battlesApi } from '../api/battles'
import client from '../api/client'

const route = useRoute()
const battle = ref(null)
const question = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    battle.value = await battlesApi.get(route.params.id)
    if (battle.value.question_id) {
      question.value = await client.get(`/questions/${battle.value.question_id}`)
    }
  } finally {
    loading.value = false
  }
})
</script>
