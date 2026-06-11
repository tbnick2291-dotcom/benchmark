import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

client.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error?.response?.data?.detail ?? error.message)
)

export default client
