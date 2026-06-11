import client from './client'

export const tasksApi = {
  list: () => client.get('/tasks'),
  get: (id) => client.get(`/tasks/${id}`),
  create: (payload) => client.post('/tasks', payload),
  start: (id) => client.post(`/tasks/${id}/start`),
}
