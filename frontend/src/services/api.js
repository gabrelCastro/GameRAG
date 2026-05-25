import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api',
})

api.interceptors.request.use((config) => {
  const access = localStorage.getItem('access')
  if (access) {
    config.headers.Authorization = `Bearer ${access}`
  }
  return config
})

let refreshing = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const refresh = localStorage.getItem('refresh')

    if (error.response?.status !== 401 || original._retry || !refresh) {
      return Promise.reject(error)
    }

    original._retry = true
    refreshing ??= axios
      .post(`${api.defaults.baseURL}/auth/token/refresh/`, { refresh })
      .then(({ data }) => {
        localStorage.setItem('access', data.access)
        return data.access
      })
      .catch((err) => {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        throw err
      })
      .finally(() => {
        refreshing = null
      })

    const access = await refreshing
    original.headers.Authorization = `Bearer ${access}`
    return api(original)
  },
)

export default api
