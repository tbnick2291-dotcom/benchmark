import { defineStore } from 'pinia'
import { tasksApi } from '../api/tasks'

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTasks() {
      this.loading = true
      this.error = null
      try {
        this.tasks = await tasksApi.list()
      } catch (e) {
        this.error = e
      } finally {
        this.loading = false
      }
    },
    async createTask(payload) {
      const task = await tasksApi.create(payload)
      this.tasks.unshift(task)
      return task
    },
    async startTask(id) {
      await tasksApi.start(id)
      const task = this.tasks.find((t) => t.id === id)
      if (task) task.status = 'running'
    },
  },
})
