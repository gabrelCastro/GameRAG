import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('access') ?? '')
  const refresh = ref(localStorage.getItem('refresh') ?? '')
  const username = ref(localStorage.getItem('username') ?? '')

  const isAuthenticated = computed(() => Boolean(access.value))

  function setTokens({ access: a, refresh: r }) {
    access.value = a
    refresh.value = r
    localStorage.setItem('access', a)
    localStorage.setItem('refresh', r)
  }

  function setUsername(u) {
    username.value = u
    localStorage.setItem('username', u)
  }

  async function login({ username: u, password }) {
    const { data } = await api.post('/auth/login/', { username: u, password })
    setTokens(data)
    setUsername(u)
  }

  async function register({ username: u, email, password }) {
    await api.post('/auth/register/', { username: u, email, password })
    await login({ username: u, password })
  }

  function logout() {
    access.value = ''
    refresh.value = ''
    username.value = ''
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('username')
  }

  return { access, refresh, username, isAuthenticated, login, register, logout }
})
