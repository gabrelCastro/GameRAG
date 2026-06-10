<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Header from '@/components/Header.vue'
import GameCard from '@/components/GameCard.vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const user = ref({ username: '', email: '' })
const favorites = ref([])
const status = ref('loading')
const errorMessage = ref('')

async function loadProfile() {
  status.value = 'loading'
  errorMessage.value = ''
  try {
    const [{ data: userData }, { data: favoriteResponse }] = await Promise.all([
      api.get('/auth/me/'),
      api.get('/games/favorites/'),
    ])

    user.value = userData
    favorites.value = favoriteResponse.map((favorite) => favorite.game)
    status.value = 'success'
  } catch (err) {
    status.value = 'error'
    errorMessage.value =
      err.response?.data?.detail ?? 'Não foi possível carregar os dados do perfil.'
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

onMounted(loadProfile)
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-950 text-gray-900 dark:text-slate-100">
    <Header
      :username="auth.username || 'Usuário'"
      @profile-click="openProfile"
      @settings-click="openSettings"
      @logout="logout"
    />

    <main class="max-w-6xl mx-auto px-4 py-10 sm:px-6 lg:px-8">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
        <div>
          <p class="text-sm uppercase tracking-[0.25em] text-sky-500 dark:text-sky-400 mb-2">Perfil</p>
          <h1 class="text-3xl font-bold text-slate-950 dark:text-white">Seu perfil</h1>
          <p class="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">
            Confira seus dados e seus jogos favoritos neste espaço.
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

      <section class="grid gap-6 lg:grid-cols-[1fr_1.4fr]">
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <h2 class="text-xl font-semibold text-slate-950 dark:text-white mb-4">Dados do usuário</h2>
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
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Jogos favoritos</h2>
              <p class="text-sm text-slate-500 dark:text-slate-400">Seus títulos marcados como favoritos.</p>
            </div>
          </div>

          <div v-if="status === 'loading'" class="text-slate-500 py-10 text-center">
            Carregando favoritos...
          </div>
          <div v-else-if="status === 'error'" class="text-rose-500 py-10 text-center">
            {{ errorMessage }}
          </div>
          <div v-else>
            <div v-if="!favorites.length" class="text-slate-500 py-10 text-center">
              Você ainda não tem jogos favoritados.
            </div>
            <ul v-else class="space-y-4">
              <li v-for="game in favorites" :key="game.id">
                <GameCard
                  class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900"
                  :game="game"
                  :show-price="false"
                />
              </li>
            </ul>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
