import { defineStore } from 'pinia'
import { leaderboardApi } from '../api/leaderboard'

export const useLeaderboardStore = defineStore('leaderboard', {
  state: () => ({
    entries: [],
    dimension: null,
    loading: false,
  }),
  actions: {
    async fetch(dimension) {
      this.loading = true
      this.dimension = dimension || null
      try {
        this.entries = await leaderboardApi.get(dimension)
      } finally {
        this.loading = false
      }
    },
  },
})
