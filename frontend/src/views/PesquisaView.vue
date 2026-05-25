<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

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
  if (!term) {
    games.value = []
    status.value = 'empty-query'
    return
  }

  status.value = 'loading'
  errorMessage.value = ''
  try {
    const { data } = await api.get('/games/', { params: { search: term } })
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

function formatPrice(value) {
  const number = Number(value)
  if (Number.isNaN(number)) return value
  return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
    <div class="max-w-5xl mx-auto px-6 py-12">
      <header class="text-center mb-8">
        <h1 class="text-4xl font-bold mb-2">Pesquisa de Jogos</h1>
        <p class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Encontre jogos por nome, gênero, plataforma ou descrição. Use a busca para explorar a
          biblioteca do GameRAG.
        </p>
      </header>

      <section class="flex flex-wrap gap-3 mb-8">
        <input
          v-model="query"
          type="text"
          placeholder="Digite o nome do jogo, gênero ou plataforma"
          class="flex-1 min-w-[320px] px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
          @keyup.enter="search"
        />
        <button
          type="button"
          class="px-5 py-3 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-medium transition-colors disabled:opacity-60"
          :disabled="status === 'loading'"
          @click="search"
        >
          {{ status === 'loading' ? 'Buscando…' : 'Pesquisar' }}
        </button>
        <button
          type="button"
          class="px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
          @click="logout"
        >
          Sair
        </button>
      </section>

      <section>
        <div
          v-if="status === 'idle'"
          class="text-center text-gray-500 dark:text-gray-400 py-10"
        >
          Nenhum jogo carregado. Faça uma pesquisa para ver resultados.
        </div>
        <div
          v-else-if="status === 'empty-query'"
          class="text-center text-gray-500 dark:text-gray-400 py-10"
        >
          Digite um termo de pesquisa para buscar jogos.
        </div>
        <div
          v-else-if="status === 'loading'"
          class="text-center text-gray-500 dark:text-gray-400 py-10"
        >
          Buscando jogos para "{{ query }}"…
        </div>
        <div
          v-else-if="status === 'error'"
          class="text-center text-red-500 dark:text-red-400 py-10"
        >
          {{ errorMessage }}
        </div>
        <div
          v-else-if="status === 'no-results'"
          class="text-center text-gray-500 dark:text-gray-400 py-10"
        >
          Nenhum jogo encontrado para "{{ query }}".
        </div>
        <div
          v-else
          class="grid gap-5 grid-cols-[repeat(auto-fill,minmax(240px,1fr))]"
        >
          <article
            v-for="game in games"
            :key="game.id"
            class="flex flex-col gap-2 p-5 rounded-2xl bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800"
          >
            <h2 class="text-lg font-semibold">{{ game.title }}</h2>
            <p class="text-sm text-gray-600 dark:text-gray-300 line-clamp-4">
              {{ game.description }}
            </p>
            <div
              class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-auto pt-2"
            >
              <span>{{ game.genre }} · {{ game.platform }}</span>
              <span>{{ formatPrice(game.price) }}</span>
            </div>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>
