import client from './client'

export const reportsApi = {
  list: () => client.get('/reports'),
  get: (id) => client.get(`/reports/${id}`),
  generate: (payload) => client.post('/reports', payload),
}
