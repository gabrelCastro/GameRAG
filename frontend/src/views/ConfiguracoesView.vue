<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Header from '@/components/Header.vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const user = ref({ username: '', email: '' })
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const status = ref('loading')

const passwordMismatch = computed(
  () => confirmPassword.value.length > 0 && newPassword.value !== confirmPassword.value,
)
const successMessage = ref('')
const errorMessage = ref('')

async function loadUser() {
  status.value = 'loading'
  errorMessage.value = ''
  try {
    const { data } = await api.get('/auth/me/')
    user.value = data
    status.value = 'success'
  } catch (err) {
    status.value = 'error'
    errorMessage.value =
      err.response?.data?.detail ?? 'Não foi possível carregar os dados de configurações.'
  }
}

async function changePassword() {
  successMessage.value = ''
  errorMessage.value = ''
  try {
    const { data } = await api.post('/auth/change-password/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
      confirm_password: confirmPassword.value,
    })
    successMessage.value = data.detail || 'Senha atualizada com sucesso.'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (err) {
    const apiError = err.response?.data
    errorMessage.value =
      apiError?.detail ||
      Object.values(apiError || {}).flat().join(' ') ||
      'Não foi possível atualizar a senha.'
  }
}

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}

function openProfile() {
  router.push({ name: 'perfil' })
}

function openSettings() {
  router.push({ name: 'configuracoes' })
}

function goBack() {
  router.push({ name: 'pesquisa' })
}

onMounted(loadUser)
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-950 text-gray-900 dark:text-gray-100">
    <Header
      :username="auth.username || 'Usuário'"
      @profile-click="openProfile"
      @settings-click="openSettings"
      @logout="logout"
      @pesquisa="goBack"
    />

    <main class="max-w-5xl mx-auto px-4 py-6 sm:px-6 sm:py-10 lg:px-8">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
        <div>
          <p class="text-sm uppercase tracking-[0.25em] text-sky-500 dark:text-sky-400 mb-2">Configurações</p>
          <h1 class="text-3xl font-bold text-slate-950 dark:text-white">Ajustes da conta</h1>
          <p class="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">
            Gerencie as informações do seu usuário e atualize sua senha de acordo com as regras do projeto.
          </p>
        </div>
        <button
          type="button"
          class="inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-5 py-3 text-sm font-medium text-slate-950 transition hover:border-slate-400 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:border-slate-600"
          @click="goBack"
        >
          Voltar para Pesquisa
        </button>
      </div>

      <section class="grid gap-4 sm:gap-6 lg:grid-cols-[1fr_1.2fr]">
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <h2 class="text-xl font-semibold text-slate-950 dark:text-white mb-4">Dados da conta</h2>
          <div class="space-y-4 text-sm text-slate-600 dark:text-slate-300">
            <div>
              <p class="font-medium text-slate-900 dark:text-white">Nome de usuário</p>
              <p>{{ user.username || '—' }}</p>
            </div>
            <div>
              <p class="font-medium text-slate-900 dark:text-white">E-mail</p>
              <p>{{ user.email || '—' }}</p>
            </div>
          </div>
        </div>

        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <div class="mb-4">
            <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Trocar senha</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400">A senha precisa ter no mínimo 8 caracteres e obedecer às regras do Django.</p>
          </div>

          <form class="space-y-4" @submit.prevent="changePassword">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-900 dark:text-slate-200">Senha atual</label>
              <div class="relative">
                <input
                  :type="showCurrentPassword ? 'text' : 'password'"
                  v-model="currentPassword"
                  class="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 pr-11 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:placeholder-slate-500"
                  required
                />
                <button
                  type="button"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                  :aria-label="showCurrentPassword ? 'Ocultar senha' : 'Mostrar senha'"
                  @click="showCurrentPassword = !showCurrentPassword"
                >
                  <svg v-if="showCurrentPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-900 dark:text-slate-200">Nova senha</label>
              <div class="relative">
                <input
                  :type="showNewPassword ? 'text' : 'password'"
                  v-model="newPassword"
                  class="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 pr-11 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:placeholder-slate-500"
                  required
                  minlength="8"
                />
                <button
                  type="button"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                  :aria-label="showNewPassword ? 'Ocultar senha' : 'Mostrar senha'"
                  @click="showNewPassword = !showNewPassword"
                >
                  <svg v-if="showNewPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-900 dark:text-slate-200">Confirmar nova senha</label>
              <div class="relative">
                <input
                  :type="showConfirmPassword ? 'text' : 'password'"
                  v-model="confirmPassword"
                  :class="[
                    'w-full rounded-2xl border px-4 py-3 pr-11 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 dark:text-slate-100 dark:placeholder-slate-500',
                    passwordMismatch
                      ? 'border-rose-400 bg-rose-50 focus:ring-rose-400 dark:border-rose-700 dark:bg-slate-950'
                      : 'border-slate-300 bg-white focus:ring-sky-500 dark:border-slate-700 dark:bg-slate-950',
                  ]"
                  required
                  minlength="8"
                />
                <button
                  type="button"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                  :aria-label="showConfirmPassword ? 'Ocultar senha' : 'Mostrar senha'"
                  @click="showConfirmPassword = !showConfirmPassword"
                >
                  <svg v-if="showConfirmPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
              <p v-if="passwordMismatch" class="mt-1 text-xs text-rose-500">As senhas não coincidem.</p>
            </div>

            <div class="space-y-3">
              <p v-if="successMessage" class="text-sm text-emerald-600">{{ successMessage }}</p>
              <p v-if="errorMessage" class="text-sm text-rose-500">{{ errorMessage }}</p>
            </div>

            <button
              type="submit"
              :disabled="passwordMismatch"
              class="inline-flex items-center justify-center rounded-2xl bg-sky-500 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Atualizar senha
            </button>
          </form>
        </div>
      </section>
    </main>
  </div>
</template>
