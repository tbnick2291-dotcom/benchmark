import { defineStore } from 'pinia'
import { modelsApi } from '../api/models'

export const useModelsStore = defineStore('models', {
  state: () => ({
    models: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchModels() {
      this.loading = true
      this.error = null
      try {
        this.models = await modelsApi.list()
      } catch (e) {
        this.error = e
      } finally {
        this.loading = false
      }
    },
    async createModel(payload) {
      const model = await modelsApi.create(payload)
      this.models.push(model)
      return model
    },
    async updateStatus(id, status) {
      const updated = await modelsApi.updateStatus(id, status)
      const idx = this.models.findIndex((m) => m.id === id)
      if (idx !== -1) this.models[idx] = updated
    },
  },
})
