import client from './client'

export const modelsApi = {
  list: () => client.get('/models'),
  get: (id) => client.get(`/models/${id}`),
  create: (payload) => client.post('/models', payload),
  updateStatus: (id, status) => client.patch(`/models/${id}/status`, { status }),
}
