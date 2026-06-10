<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import Header from '@/components/Header.vue'
import GameCard from '@/components/GameCard.vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const query = ref('')
const games = ref([])
const status = ref('idle')
const errorMessage = ref('')

async function search() {
  const term = query.value.trim()

  status.value = 'loading'
  errorMessage.value = ''
  try {
    const params = term ? { search: term } : {}
    const { data } = await api.get('/games/', { params })
    games.value = Array.isArray(data) ? data : (data.results ?? [])
    status.value = games.value.length ? 'success' : 'no-results'
  } catch (err) {
    status.value = 'error'
    errorMessage.value =
      err.response?.data?.detail ?? 'Não foi possível buscar os jogos no momento.'
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

function openPesquisa() {
  router.push({ name: 'pesquisa' })
}

function formatPrice(value) {
  const number = Number(value)
  if (Number.isNaN(number)) return value
  return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
    <Header
      :username="auth.username || 'Usuário'"
      @profile-click="openProfile"
      @settings-click="openSettings"
      @logout="logout"
      @pesquisa="openPesquisa"
    />
    <main id="search-page" aria-labelledby="search-heading" class="max-w-6xl mx-auto px-4 py-10 sm:px-6 lg:px-8">
      <section class="mx-auto w-full max-w-4xl rounded-[2rem] border border-slate-200/40 bg-white/90 p-6 shadow-xl shadow-slate-950/10 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95 dark:shadow-slate-950/40">
        <div class="text-center mb-8">
          <p class="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-sky-400/80 mb-3">Pesquisa de Jogos</p>
          <h1 id="search-heading" class="text-4xl sm:text-5xl font-semibold text-slate-950 dark:text-white mb-3">Encontre seu próximo jogo</h1>
          <p class="text-slate-600 max-w-2xl mx-auto leading-7 dark:text-slate-300">
            Encontre jogos por nome, gênero, plataforma ou descrição. Use a busca para explorar a
            biblioteca do GameRAG.
          </p>
        </div>

        <section class="mb-8">
          <form class="grid gap-3 sm:grid-cols-[1.8fr_auto] sm:items-end" @submit.prevent="search" aria-label="Busca de jogos">
            <label class="sr-only" for="search-input">Buscar jogos por nome, gênero ou plataforma</label>
            <input
              id="search-input"
              v-model="query"
              type="search"
              placeholder="Digite o nome do jogo, gênero ou plataforma"
              class="w-full px-5 py-4 rounded-2xl border border-slate-300 bg-white text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:placeholder-slate-500"
              @keyup.enter="search"
              aria-label="Buscar jogos por nome, gênero ou plataforma"
            />
            <button
              type="submit"
              class="w-full sm:w-auto px-6 py-4 rounded-2xl bg-sky-500 hover:bg-sky-400 text-white font-semibold transition-all shadow-lg shadow-sky-500/20 dark:shadow-sky-500/20 disabled:opacity-60"
              :disabled="status === 'loading'"
            >
              {{ status === 'loading' ? 'Buscando…' : 'Pesquisar' }}
            </button>
          </form>
        </section>
      </section>

      <section aria-live="polite" aria-atomic="true" class="min-h-[5rem] mt-8">
        <div
          v-if="status === 'idle'"
          role="status"
          class="text-center text-slate-400 py-10"
        >
          Nenhum jogo carregado. Faça uma pesquisa para ver resultados.
        </div>
        <div
          v-else-if="status === 'empty-query'"
          class="text-center text-slate-400 py-10"
        >
          Digite um termo de pesquisa para buscar jogos.
        </div>
        <div
          v-else-if="status === 'loading'"
          role="status"
          class="text-center text-slate-400 py-10"
        >
          Buscando jogos para "{{ query }}"…
        </div>
        <div
          v-else-if="status === 'error'"
          class="text-center text-rose-400 py-10"
        >
          {{ errorMessage }}
        </div>
        <div
          v-else-if="status === 'no-results'"
          class="text-center text-slate-400 py-10"
        >
          Nenhum jogo encontrado para "{{ query }}".
        </div>
        <div
          v-else
          class="grid gap-6 sm:grid-cols-2 xl:grid-cols-3"
        >
          <GameCard
            v-for="game in games"
            :key="game.id"
            :game="game"
          />
        </div>
      </section>
    </main>
  </div>
</template>
