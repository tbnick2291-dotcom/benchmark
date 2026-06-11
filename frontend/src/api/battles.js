import client from './client'

export const battlesApi = {
  list: () => client.get('/battles'),
  get: (id) => client.get(`/battles/${id}`),
}
