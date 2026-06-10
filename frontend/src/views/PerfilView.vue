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
const library = ref([])
const status = ref('loading')
const errorMessage = ref('')

const statusLabels = {
  want_to_play: 'Quero jogar',
  playing: 'Jogando',
  completed: 'Concluído',
  dropped: 'Abandonado',
}

const statusOrder = ['playing', 'completed', 'want_to_play', 'dropped']

const librarySummary = computed(() => {
  const counts = {
    want_to_play: 0,
    playing: 0,
    completed: 0,
    dropped: 0,
  }
  let totalHours = 0

  library.value.forEach((entry) => {
    counts[entry.status] += 1
    totalHours += Number(entry.hours_played) || 0
  })

  return {
    totalGames: library.value.length,
    ...counts,
    totalHours,
  }
})

const groupedLibrary = computed(() =>
  statusOrder.map((key) => ({
    status: key,
    label: statusLabels[key],
    entries: library.value.filter((entry) => entry.status === key),
  }))
)

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
    library.value = libraryResponse
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
          <p class="text-sm uppercase tracking-[0.25em] text-sky-500 dark:text-sky-400 mb-2">Biblioteca</p>
          <h1 class="text-3xl font-bold text-slate-950 dark:text-white">Sua biblioteca de jogos</h1>
          <p class="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">
            Acompanhe seus jogos favoritos, os títulos que você está jogando, os que concluiu e os que pretende jogar.
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

      <section class="grid gap-6 xl:grid-cols-[1.3fr_0.9fr]">
        <div class="space-y-6">
          <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <article class="rounded-[1.75rem] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
              <p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Jogos na biblioteca</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950 dark:text-white">{{ librarySummary.totalGames }}</p>
            </article>
            <article class="rounded-[1.75rem] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
              <p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Jogando</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950 dark:text-white">{{ librarySummary.playing }}</p>
            </article>
            <article class="rounded-[1.75rem] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
              <p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Concluídos</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950 dark:text-white">{{ librarySummary.completed }}</p>
            </article>
            <article class="rounded-[1.75rem] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
              <p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">Horas jogadas</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950 dark:text-white">{{ librarySummary.totalHours }}</p>
            </article>
          </div>

          <section class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
            <div class="flex flex-col gap-1 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 class="text-xl font-semibold text-slate-950 dark:text-white">Status da sua biblioteca</h2>
                <p class="text-sm text-slate-500 dark:text-slate-400">Veja em quais jogos você está jogando, quer jogar ou já concluiu.</p>
              </div>
            </div>

            <div v-if="status === 'loading'" class="py-10 text-center text-slate-500">
              Carregando sua biblioteca...
            </div>
            <div v-else-if="status === 'error'" class="py-10 text-center text-rose-500">
              {{ errorMessage }}
            </div>
            <div v-else>
              <div v-if="!library.length" class="py-10 text-center text-slate-500">
                Sua biblioteca está vazia. Busque jogos e adicione-os à sua lista.
              </div>

              <div v-else class="space-y-6">
                <div v-for="group in groupedLibrary" :key="group.status" v-if="group.entries.length">
                  <div class="rounded-3xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
                    <div class="flex items-center justify-between gap-3">
                      <div>
                        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">{{ group.label }}</p>
                        <p class="text-3xl font-semibold text-slate-950 dark:text-white">{{ group.entries.length }}</p>
                      </div>
                      <span class="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                        {{ statusLabels[group.status] }}
                      </span>
                    </div>
                  </div>

                  <ul class="space-y-4">
                    <li
                      v-for="entry in group.entries"
                      :key="entry.id"
                      class="rounded-[1.5rem] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20"
                    >
                      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                        <div>
                          <p class="text-lg font-semibold text-slate-950 dark:text-white">{{ entry.game.title }}</p>
                          <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
                            {{ entry.game.genre }} · {{ entry.game.platform }}
                          </p>
                        </div>
                        <div class="flex items-center gap-3 text-sm text-slate-600 dark:text-slate-300">
                          <span class="rounded-full bg-slate-100 px-3 py-1 text-slate-700 dark:bg-slate-800 dark:text-slate-200">
                            {{ statusLabels[entry.status] }}
                          </span>
                          <span>
                            {{ Number(entry.hours_played).toLocaleString('pt-BR') }} horas
                          </span>
                        </div>
                      </div>
                      <p class="mt-4 text-sm leading-6 text-slate-600 dark:text-slate-400 line-clamp-2">
                        {{ entry.game.description }}
                      </p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </section>
        </div>

        <aside class="space-y-6">
          <section class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
            <h2 class="text-xl font-semibold text-slate-950 dark:text-white mb-3">Seus favoritos</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400 mb-4">
              Jogos que você marcou como favoritos para voltar a jogar ou guardar como referência.
            </p>

            <div v-if="status === 'loading'" class="py-10 text-center text-slate-500">
              Carregando favoritos...
            </div>
            <div v-else-if="status === 'error'" class="py-10 text-center text-rose-500">
              {{ errorMessage }}
            </div>
            <div v-else>
              <div v-if="!favorites.length" class="text-center text-slate-500">
                Nenhum favorito salvo ainda.
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
          </section>

          <section class="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/20">
            <h2 class="text-xl font-semibold text-slate-950 dark:text-white mb-3">O que você pode fazer</h2>
            <ul class="space-y-3 text-sm text-slate-600 dark:text-slate-300">
              <li class="flex items-start gap-2">
                <span class="mt-1 inline-flex h-2.5 w-2.5 rounded-full bg-sky-500"></span>
                Favoritar jogos para encontrá-los rápido.
              </li>
              <li class="flex items-start gap-2">
                <span class="mt-1 inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
                Marcar o status de cada jogo: jogando, concluído, parado ou quero jogar.
              </li>
              <li class="flex items-start gap-2">
                <span class="mt-1 inline-flex h-2.5 w-2.5 rounded-full bg-amber-500"></span>
                Avaliar e comentar jogos diretamente na página de detalhes.
              </li>
            </ul>
          </section>
        </aside>
      </section>
    </main>
  </div>
</template>
