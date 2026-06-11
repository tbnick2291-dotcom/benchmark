import client from './client'

export const systemApi = {
  health: () => client.get('/system/health'),
  status: () => client.get('/system/status'),
}
