import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('access') ?? '')
  const refresh = ref(localStorage.getItem('refresh') ?? '')

  const isAuthenticated = computed(() => Boolean(access.value))

  function setTokens({ access: a, refresh: r }) {
    access.value = a
    refresh.value = r
    localStorage.setItem('access', a)
    localStorage.setItem('refresh', r)
  }

  async function login({ username, password }) {
    const { data } = await api.post('/auth/login/', { username, password })
    setTokens(data)
  }

  async function register({ username, email, password }) {
    await api.post('/auth/register/', { username, email, password })
    await login({ username, password })
  }

  function logout() {
    access.value = ''
    refresh.value = ''
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
  }

  return { access, refresh, isAuthenticated, login, register, logout }
})
