<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Header from '@/components/Header.vue'
import GameCard from '@/components/GameCard.vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const user = ref({ username: '', email: '' })
const favorites = ref([])
const libraryEntries = ref([])
const status = ref('loading')
const errorMessage = ref('')

const libraryGroups = computed(() => {
  return libraryEntries.value.reduce(
    (groups, entry) => {
      if (entry.status in groups) {
        groups[entry.status].push(entry)
      }
      return groups
    },
    { completed: [], playing: [], want_to_play: [], dropped: [] },
  )
})

const libraryCounts = computed(() => ({
  completed: libraryGroups.value.completed.length,
  playing: libraryGroups.value.playing.length,
  want_to_play: libraryGroups.value.want_to_play.length,
  dropped: libraryGroups.value.dropped.length,
  total: libraryEntries.value.length,
}))

const libraryHours = computed(() => {
  const sumHours = (entries) =>
    entries.reduce((sum, entry) => sum + Number(entry.hours_played ?? 0), 0)

  return {
    completed: sumHours(libraryGroups.value.completed),
    playing: sumHours(libraryGroups.value.playing),
    want_to_play: sumHours(libraryGroups.value.want_to_play),
    dropped: sumHours(libraryGroups.value.dropped),
    total: sumHours(libraryEntries.value),
  }
})

const favoriteCount = computed(() => favorites.value.length)
const totalHoursPlayed = computed(() => libraryHours.value.total)

async function loadProfile() {
  status.value = 'loading'
  errorMessage.value = ''

  try {
    const [{ data: userData }, { data: favoriteResponse }, { data: libraryResponse }] = await Promise.all([
      api.get('/auth/me/'),
      api.get('/games/favorites/'),
      api.get('/games/library/'),
    ])

    user.value = userData
    favorites.value = favoriteResponse.map((favorite) => favorite.game)
    libraryEntries.value = libraryResponse
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
      @settings-click="openSettings"
      @logout="logout"
      @pesquisa="goBack"
    />

    <main class="max-w-6xl mx-auto px-4 py-6 sm:px-6 sm:py-10 lg:px-8 space-y-8">

      <!-- Cabeçalho da página -->
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm uppercase tracking-[0.25em] text-sky-500 dark:text-sky-400 mb-2">Perfil</p>
          <h1 class="text-3xl font-bold text-slate-950 dark:text-white">Seu perfil</h1>
          <p class="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">
            Veja seu progresso, favoritos e status dos jogos na sua biblioteca.
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

      <!-- Bloco 1: Informações e estatísticas do usuário -->
      <section class="grid gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-4">

        <!-- Dados do usuário -->
        <div class="sm:col-span-2 lg:col-span-2 rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <h2 class="text-xl font-semibold text-slate-950 dark:text-white mb-4">Dados do usuário</h2>

          <div v-if="status === 'loading'" class="animate-pulse space-y-4">
            <div>
              <div class="mb-1 h-3 w-28 rounded bg-slate-200 dark:bg-slate-700"></div>
              <div class="h-4 w-40 rounded bg-slate-200 dark:bg-slate-700"></div>
            </div>
            <div>
              <div class="mb-1 h-3 w-16 rounded bg-slate-200 dark:bg-slate-700"></div>
              <div class="h-4 w-52 rounded bg-slate-200 dark:bg-slate-700"></div>
            </div>
          </div>

          <div v-else class="space-y-4 text-sm text-slate-600 dark:text-slate-300">
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

        <!-- Card: Favoritos -->
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20 flex flex-col justify-between">
          <p class="text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Favoritos</p>
          <div v-if="status === 'loading'" class="animate-pulse mt-2 h-8 w-16 rounded bg-slate-200 dark:bg-slate-700"></div>
          <p v-else class="mt-2 text-4xl font-semibold text-slate-950 dark:text-white">{{ favoriteCount }}</p>
        </div>

        <!-- Card: Horas totais -->
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20 flex flex-col justify-between">
          <p class="text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Horas jogadas</p>
          <div v-if="status === 'loading'" class="animate-pulse mt-2 h-8 w-16 rounded bg-slate-200 dark:bg-slate-700"></div>
          <p v-else class="mt-2 text-4xl font-semibold text-slate-950 dark:text-white">{{ totalHoursPlayed.toFixed(1) }}</p>
        </div>

      </section>

      <!-- Bloco 2: Estatísticas da biblioteca -->
      <section class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
        <div class="flex items-start justify-between gap-4 mb-6">
          <div>
            <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Minha Biblioteca</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400">Visão geral do seu progresso e status dos jogos.</p>
          </div>
          <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-slate-700 dark:bg-slate-800 dark:text-slate-300">
            {{ libraryCounts.total }} jogos
          </span>
        </div>

        <div v-if="status === 'loading'" class="animate-pulse grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="i in 4" :key="i" class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
        </div>

        <div v-else class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
            <p class="text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Concluídos</p>
            <p class="mt-2 text-2xl font-semibold text-emerald-600 dark:text-emerald-400">{{ libraryCounts.completed }}</p>
            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ libraryHours.completed.toFixed(1) }} h</p>
          </div>
          <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
            <p class="text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Em andamento</p>
            <p class="mt-2 text-2xl font-semibold text-sky-600 dark:text-sky-400">{{ libraryCounts.playing }}</p>
            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ libraryHours.playing.toFixed(1) }} h</p>
          </div>
          <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
            <p class="text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Quero jogar</p>
            <p class="mt-2 text-2xl font-semibold text-violet-600 dark:text-violet-400">{{ libraryCounts.want_to_play }}</p>
            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ libraryHours.want_to_play.toFixed(1) }} h</p>
          </div>
          <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
            <p class="text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Dropados</p>
            <p class="mt-2 text-2xl font-semibold text-rose-600 dark:text-rose-400">{{ libraryCounts.dropped }}</p>
            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ libraryHours.dropped.toFixed(1) }} h</p>
          </div>
        </div>
      </section>

      <!-- Bloco 3: Jogos favoritos -->
      <section class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Jogos favoritos</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400">Seus títulos marcados como favoritos.</p>
          </div>
          <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-slate-700 dark:bg-slate-800 dark:text-slate-300">
            {{ favoriteCount }}
          </span>
        </div>

        <div v-if="status === 'loading'" class="animate-pulse space-y-4">
          <div
            v-for="i in 3"
            :key="i"
            class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900"
          >
            <div class="mb-2 h-4 w-3/4 rounded bg-slate-200 dark:bg-slate-700"></div>
            <div class="mb-1 h-3 w-1/2 rounded bg-slate-200 dark:bg-slate-700"></div>
            <div class="h-3 w-1/3 rounded bg-slate-200 dark:bg-slate-700"></div>
          </div>
        </div>
        <div v-else-if="status === 'error'" class="text-rose-500 py-10 text-center">
          {{ errorMessage }}
        </div>
        <div v-else>
          <div v-if="!favorites.length" class="text-slate-500 py-10 text-center">
            Você ainda não tem jogos favoritados.
          </div>
          <ul v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <li v-for="game in favorites" :key="game.id">
              <GameCard
                class="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900 h-full"
                :game="game"
                :show-price="false"
              />
            </li>
          </ul>
        </div>
      </section>

      <!-- Bloco 4: Jogos da biblioteca por status -->
      <section class="grid gap-4 sm:gap-6 lg:grid-cols-2">

        <!-- Concluídos -->
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Concluídos</h2>
              <p class="text-sm text-slate-500 dark:text-slate-400">Jogos finalizados na sua biblioteca.</p>
            </div>
            <span class="rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300">
              {{ libraryCounts.completed }}
            </span>
          </div>
          <div v-if="status === 'loading'" class="animate-pulse space-y-4">
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
          </div>
          <div v-else-if="!libraryGroups.completed.length" class="text-slate-500 py-10 text-center">
            Nenhum jogo concluído ainda.
          </div>
          <ul v-else class="space-y-4">
            <li v-for="entry in libraryGroups.completed" :key="entry.id">
              <div class="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
                <GameCard :game="entry.game" :show-price="false" />
                <p class="text-sm text-slate-500 dark:text-slate-400">Horas jogadas: {{ Number(entry.hours_played).toFixed(1) }}</p>
              </div>
            </li>
          </ul>
        </div>

        <!-- Em andamento -->
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Em andamento</h2>
              <p class="text-sm text-slate-500 dark:text-slate-400">Jogos que você está jogando atualmente.</p>
            </div>
            <span class="rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300">
              {{ libraryCounts.playing }}
            </span>
          </div>
          <div v-if="status === 'loading'" class="animate-pulse space-y-4">
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
          </div>
          <div v-else-if="!libraryGroups.playing.length" class="text-slate-500 py-10 text-center">
            Nenhum jogo em andamento.
          </div>
          <ul v-else class="space-y-4">
            <li v-for="entry in libraryGroups.playing" :key="entry.id">
              <div class="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
                <GameCard :game="entry.game" :show-price="false" />
                <p class="text-sm text-slate-500 dark:text-slate-400">Horas jogadas: {{ Number(entry.hours_played).toFixed(1) }}</p>
              </div>
            </li>
          </ul>
        </div>

        <!-- Quero jogar -->
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Quero jogar</h2>
              <p class="text-sm text-slate-500 dark:text-slate-400">Jogos que você pretende iniciar em breve.</p>
            </div>
            <span class="rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300">
              {{ libraryCounts.want_to_play }}
            </span>
          </div>
          <div v-if="status === 'loading'" class="animate-pulse space-y-4">
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
          </div>
          <div v-else-if="!libraryGroups.want_to_play.length" class="text-slate-500 py-10 text-center">
            Nenhum jogo marcado como quero jogar.
          </div>
          <ul v-else class="space-y-4">
            <li v-for="entry in libraryGroups.want_to_play" :key="entry.id">
              <div class="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
                <GameCard :game="entry.game" :show-price="false" />
                <p class="text-sm text-slate-500 dark:text-slate-400">Horas jogadas: {{ Number(entry.hours_played ?? 0).toFixed(1) }}</p>
              </div>
            </li>
          </ul>
        </div>

        <!-- Dropados -->
        <div class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Dropados</h2>
              <p class="text-sm text-slate-500 dark:text-slate-400">Jogos que você abandonou ou pausou definitivamente.</p>
            </div>
            <span class="rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-300">
              {{ libraryCounts.dropped }}
            </span>
          </div>
          <div v-if="status === 'loading'" class="animate-pulse space-y-4">
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
            <div class="h-24 rounded-2xl bg-slate-200 dark:bg-slate-700"></div>
          </div>
          <div v-else-if="!libraryGroups.dropped.length" class="text-slate-500 py-10 text-center">
            Nenhum jogo abandonado.
          </div>
          <ul v-else class="space-y-4">
            <li v-for="entry in libraryGroups.dropped" :key="entry.id">
              <div class="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
                <GameCard :game="entry.game" :show-price="false" />
                <p class="text-sm text-slate-500 dark:text-slate-400">Horas jogadas: {{ Number(entry.hours_played).toFixed(1) }}</p>
              </div>
            </li>
          </ul>
        </div>

      </section>
    </main>
  </div>
</template>