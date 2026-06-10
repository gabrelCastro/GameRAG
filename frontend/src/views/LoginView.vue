<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import ThemeToggle from '@/components/ThemeToggle.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const currentTab = ref('login')
const submitting = ref(false)
const errorMessage = ref('')

const login = reactive({ username: '', password: '' })
const signup = reactive({ username: '', email: '', password: '', confirm: '' })

const submitLabel = computed(() => (currentTab.value === 'login' ? 'Entrar' : 'Criar Conta'))

function selectTab(tab) {
  currentTab.value = tab
  errorMessage.value = ''
}

function tabClass(tab) {
  return tab === currentTab.value
    ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
}

async function onSubmit() {
  errorMessage.value = ''

  if (currentTab.value === 'signup') {
    if (signup.password.length < 8) {
      errorMessage.value = 'A senha deve ter no mínimo 8 caracteres.'
      return
    }
    if (signup.password !== signup.confirm) {
      errorMessage.value = 'As senhas não coincidem.'
      return
    }
  }

  submitting.value = true
  try {
    if (currentTab.value === 'login') {
      await auth.login({ username: login.username, password: login.password })
    } else {
      await auth.register({
        username: signup.username,
        email: signup.email,
        password: signup.password,
      })
    }
    router.push({ name: 'pesquisa' })
  } catch (err) {
    const data = err.response?.data
    if (data?.detail) {
      errorMessage.value = data.detail
    } else if (data && typeof data === 'object') {
      const fieldLabels = { username: 'Usuário', email: 'E-mail', password: 'Senha', non_field_errors: '' }
      const messages = Object.entries(data)
        .flatMap(([field, errors]) => {
          const label = fieldLabels[field] ?? field
          return errors.map((e) => (label ? `${label}: ${e}` : e))
        })
      errorMessage.value = messages.join(' ') || 'Não foi possível concluir a operação.'
    } else {
      errorMessage.value = 'Não foi possível concluir a operação.'
    }
  } finally {
    submitting.value = false
  }
}

const inputClass =
  'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 dark:focus:ring-purple-400 transition-all'
const labelClass = 'block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300'
</script>

<template>
  <main id="login-page" aria-labelledby="login-heading" class="min-h-screen flex flex-col items-center justify-center px-4 py-12 relative">
    <div class="absolute top-4 right-4 z-20">
      <ThemeToggle />
    </div>
    <div class="w-full max-w-md">
      <div class="text-center mb-12">
        <div
          class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full mb-4"
        >
          <svg
            class="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
        </div>
        <h1
          id="login-heading"
          class="text-4xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-400 dark:to-indigo-400 bg-clip-text text-transparent mb-2"
        >
          GameRAG
        </h1>
        <p class="text-gray-600 dark:text-gray-400">Descubra seus próximos jogos favoritos</p>
      </div>

      <form class="space-y-6" @submit.prevent="onSubmit">
        <div role="tablist" aria-label="Alternar entre Entrar e Cadastrar" class="flex gap-2 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
          <button
            id="login-tab"
            role="tab"
            type="button"
            class="flex-1 py-2 px-4 rounded-md font-medium transition-all"
            :class="tabClass('login')"
            :aria-selected="currentTab === 'login'"
            aria-controls="login-panel"
            @click="selectTab('login')"
          >
            Entrar
          </button>
          <button
            id="signup-tab"
            role="tab"
            type="button"
            class="flex-1 py-2 px-4 rounded-md font-medium transition-all"
            :class="tabClass('signup')"
            :aria-selected="currentTab === 'signup'"
            aria-controls="signup-panel"
            @click="selectTab('signup')"
          >
            Cadastrar
          </button>
        </div>

        <div v-if="currentTab === 'login'" id="login-panel" role="tabpanel" aria-labelledby="login-tab" class="space-y-4">
          <div>
            <label for="login-username" :class="labelClass">Usuário</label>
            <input
              id="login-username"
              v-model="login.username"
              type="text"
              placeholder="seu_usuario"
              autocomplete="username"
              required
              :class="inputClass"
            />
          </div>
          <div>
            <label for="login-password" :class="labelClass">Senha</label>
            <input
              id="login-password"
              v-model="login.password"
              type="password"
              placeholder="••••••••"
              autocomplete="current-password"
              required
              :class="inputClass"
            />
          </div>
        </div>

        <div v-else id="signup-panel" role="tabpanel" aria-labelledby="signup-tab" class="space-y-4">
          <div>
            <label for="signup-username" :class="labelClass">Usuário</label>
            <input
              id="signup-username"
              v-model="signup.username"
              type="text"
              placeholder="seu_usuario"
              autocomplete="username"
              required
              :class="inputClass"
            />
          </div>
          <div>
            <label for="signup-email" :class="labelClass">Email</label>
            <input
              id="signup-email"
              v-model="signup.email"
              type="email"
              placeholder="seu@email.com"
              autocomplete="email"
              required
              :class="inputClass"
            />
          </div>
          <div>
            <label for="signup-password" :class="labelClass">Senha</label>
            <input
              id="signup-password"
              v-model="signup.password"
              type="password"
              placeholder="••••••••"
              autocomplete="new-password"
              required
              :class="inputClass"
            />
          </div>
          <div>
            <label for="signup-confirm" :class="labelClass">Confirmar Senha</label>
            <input
              id="signup-confirm"
              v-model="signup.confirm"
              type="password"
              placeholder="••••••••"
              autocomplete="new-password"
              required
              :class="inputClass"
            />
          </div>
        </div>

        <p v-if="errorMessage" class="text-sm text-red-500 dark:text-red-400">
          {{ errorMessage }}
        </p>

        <button
          type="submit"
          :disabled="submitting"
          class="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105 active:scale-95 shadow-lg disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100"
          :aria-busy="submitting"
        >
          {{ submitting ? 'Aguarde…' : submitLabel }}
        </button>
      </form>
    </div>
  </main>
</template>
