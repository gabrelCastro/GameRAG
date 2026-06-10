<script setup>
import { computed, ref, watch, onBeforeUnmount, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const props = defineProps({
  game: {
    type: Object,
    required: true,
  },
  showPrice: {
    type: Boolean,
    default: true,
  },
  showPlatformBadge: {
    type: Boolean,
    default: true,
  },
})

const isDetailsOpen = ref(false)
const reviews = ref([])
const userReview = ref(null)
const isFavorited = ref(false)
const reviewsLoading = ref(false)
const reviewsError = ref('')
const isSavingReview = ref(false)
const newRating = ref(5)
const newComment = ref('')
const favoriteLoading = ref(false)

const formattedPrice = computed(() => {
  const value = props.game?.price
  const number = Number(value)

  if (Number.isNaN(number)) return value ?? ''

  return number.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
})

const averageRating = computed(() => {
  if (!reviews.value.length) return 0
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  return (sum / reviews.value.length).toFixed(1)
})

async function loadReviews() {
  reviewsLoading.value = true
  reviewsError.value = ''
  try {
    const { data } = await api.get(`/games/${props.game.id}/reviews/`)
    reviews.value = data
    userReview.value = data.find((r) => r.username === auth.username) || null
    if (userReview.value) {
      newRating.value = userReview.value.rating
      newComment.value = userReview.value.comment
    }
  } catch (err) {
    reviewsError.value = 'Não foi possível carregar os reviews.'
  } finally {
    reviewsLoading.value = false
  }
}

async function checkFavorited() {
  try {
    const { data } = await api.get('/games/favorites/')
    isFavorited.value = data.some((fav) => fav.game.id === props.game.id)
  } catch (err) {
    // Falha ao verificar favoritos — mantém estado anterior
  }
}

async function saveReview() {
  isSavingReview.value = true
  try {
    await api.post(`/games/${props.game.id}/reviews/`, {
      rating: newRating.value,
      comment: newComment.value,
    })
    await loadReviews()
  } catch (err) {
    reviewsError.value = err.response?.data?.detail || 'Erro ao salvar avaliação.'
  } finally {
    isSavingReview.value = false
  }
}

async function deleteReview() {
  try {
    await api.delete(`/games/${props.game.id}/reviews/me/`)
    newRating.value = 5
    newComment.value = ''
    userReview.value = null
    await loadReviews()
  } catch (err) {
    reviewsError.value = 'Erro ao deletar avaliação.'
  }
}

async function toggleFavorite() {
  favoriteLoading.value = true
  try {
    if (isFavorited.value) {
      await api.delete(`/games/${props.game.id}/favorite/`)
    } else {
      await api.post(`/games/${props.game.id}/favorite/`)
    }
    isFavorited.value = !isFavorited.value
  } catch (err) {
    // Falha ao atualizar favorito — mantém estado anterior
  } finally {
    favoriteLoading.value = false
  }
}

function openDetails() {
  isDetailsOpen.value = true
  loadReviews()
  checkFavorited()
}

function closeDetails() {
  isDetailsOpen.value = false
}

function handleKeydown(event) {
  if (event.key === 'Escape') {
    closeDetails()
  }
}

watch(isDetailsOpen, (open) => {
  if (open) {
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', handleKeydown)
  } else {
    document.body.style.overflow = ''
    window.removeEventListener('keydown', handleKeydown)
  }
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <article
    class="flex h-full cursor-pointer flex-col gap-4 rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-lg shadow-slate-950/10 transition-all duration-200 hover:-translate-y-1 hover:shadow-xl dark:border-slate-800 dark:bg-slate-950 dark:shadow-slate-950/40"
    tabindex="0"
    role="button"
    @click="openDetails"
    @keydown.enter="openDetails"
    @keydown.space.prevent="openDetails"
  >
    <h2 class="text-lg font-semibold text-slate-950 dark:text-white">
      {{ game.title }}
    </h2>

    <p class="line-clamp-4 overflow-hidden text-sm text-slate-600 dark:text-slate-400">
      {{ game.description }}
    </p>

    <div class="mt-auto flex flex-col gap-3 text-xs text-slate-500 dark:text-slate-400 sm:text-sm">
      <span class="font-medium text-slate-700 dark:text-slate-300">
        {{ game.genre }}
        <span v-if="showPlatformBadge && game.platform">
          · {{ game.platform }}
        </span>
      </span>

      <span
        v-if="showPrice"
        class="font-semibold text-sky-500 dark:text-sky-400"
      >
        {{ formattedPrice }}
      </span>
    </div>
  </article>

  <Teleport to="body">
    <div
      v-if="isDetailsOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 p-4"
      @click.self="closeDetails"
    >
      <section
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`game-details-title-${game.id}`"
        class="max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-[1.75rem] bg-white p-6 shadow-2xl dark:bg-slate-950"
      >
        <!-- Header -->
        <div class="flex items-start justify-between gap-4 border-b border-slate-200 pb-4 dark:border-slate-800">
          <div class="flex-1">
            <h2
              :id="`game-details-title-${game.id}`"
              class="text-2xl font-bold text-slate-950 dark:text-white"
            >
              {{ game.title }}
            </h2>

            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
              {{ game.genre }}
              <span v-if="showPlatformBadge && game.platform">
                · {{ game.platform }}
              </span>
            </p>
          </div>

          <div class="flex gap-2">
            <button
              type="button"
              :disabled="favoriteLoading"
              class="rounded-full px-3 py-2 transition"
              :class="isFavorited
                ? 'bg-sky-100 text-sky-600 hover:bg-sky-200 dark:bg-sky-900 dark:text-sky-300 dark:hover:bg-sky-800'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700'
              "
              @click="toggleFavorite"
              :title="isFavorited ? 'Remover dos favoritos' : 'Adicionar aos favoritos'"
            >
              <svg
                class="h-5 w-5"
                :fill="isFavorited ? 'currentColor' : 'none'"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                />
              </svg>
            </button>

            <button
              type="button"
              class="rounded-full px-3 py-1 text-sm text-slate-500 transition hover:bg-slate-100 dark:hover:bg-slate-800"
              @click="closeDetails"
            >
              Fechar
            </button>
          </div>
        </div>

        <!-- Main Content -->
        <div class="mt-6 grid gap-6 lg:grid-cols-3">
          <!-- Left Column: Game Info -->
          <div class="space-y-5 lg:col-span-1">
            <div>
              <h3 class="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
                Descrição
              </h3>
              <p class="text-sm leading-6 text-slate-700 dark:text-slate-300">
                {{ game.description }}
              </p>
            </div>

            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
              <div>
                <h3 class="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Desenvolvedora
                </h3>
                <p class="text-sm text-slate-800 dark:text-slate-200">
                  {{ game.developer || 'Não informada' }}
                </p>
              </div>

              <div>
                <h3 class="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Publicadora
                </h3>
                <p class="text-sm text-slate-800 dark:text-slate-200">
                  {{ game.publisher || 'Não informada' }}
                </p>
              </div>

              <div>
                <h3 class="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Data de Lançamento
                </h3>
                <p class="text-sm text-slate-800 dark:text-slate-200">
                  {{ new Date(game.release_date).toLocaleDateString('pt-BR') }}
                </p>
              </div>

              <div>
                <h3 class="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Avaliação do Jogo
                </h3>
                <p class="flex items-center gap-1 text-sm font-semibold text-yellow-500">
                  ⭐ {{ game.rating }}/10
                </p>
              </div>

              <div v-if="showPrice">
                <h3 class="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Preço
                </h3>
                <p class="text-sm font-semibold text-sky-500 dark:text-sky-400">
                  {{ formattedPrice }}
                </p>
              </div>

              <div v-if="game.tags && game.tags.length">
                <h3 class="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Tags
                </h3>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="tag in game.tags"
                    :key="tag"
                    class="inline-block rounded-full bg-slate-200 px-2 py-1 text-xs text-slate-700 dark:bg-slate-800 dark:text-slate-300"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Reviews and Rating Form -->
          <div class="space-y-5 lg:col-span-2">
            <!-- Your Review Section -->
            <div class="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900">
              <h3 class="mb-3 text-sm font-semibold text-slate-900 dark:text-white">
                {{ userReview ? 'Sua Avaliação' : 'Deixe sua Avaliação' }}
              </h3>

              <div class="space-y-3">
                <div>
                  <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">
                    Nota (1-10)
                  </label>
                  <div class="flex items-center gap-2">
                    <input
                      v-model.number="newRating"
                      type="range"
                      min="1"
                      max="10"
                      class="flex-1 h-2 bg-slate-300 rounded-lg appearance-none cursor-pointer dark:bg-slate-700"
                    />
                    <span class="min-w-fit font-semibold text-slate-900 dark:text-white">
                      {{ newRating }}/10
                    </span>
                  </div>
                </div>

                <div>
                  <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">
                    Comentário (opcional)
                  </label>
                  <textarea
                    v-model="newComment"
                    rows="3"
                    class="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-500 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 dark:placeholder-slate-500"
                    placeholder="Compartilhe sua opinião sobre o jogo..."
                  />
                </div>

                <div class="flex gap-2">
                  <button
                    type="button"
                    :disabled="isSavingReview"
                    class="flex-1 rounded-lg bg-sky-500 px-3 py-2 text-sm font-semibold text-white transition hover:bg-sky-600 disabled:opacity-60 dark:bg-sky-600 dark:hover:bg-sky-700"
                    @click="saveReview"
                  >
                    {{ isSavingReview ? 'Salvando...' : (userReview ? 'Atualizar' : 'Enviar') }}
                  </button>

                  <button
                    v-if="userReview"
                    type="button"
                    class="rounded-lg border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800"
                    @click="deleteReview"
                  >
                    Deletar
                  </button>
                </div>
              </div>
            </div>

            <!-- Reviews List -->
            <div>
              <h3 class="mb-3 text-sm font-semibold text-slate-900 dark:text-white">
                Avaliações dos Usuários
                <span v-if="reviews.length" class="text-xs font-normal text-slate-500">
                  ({{ reviews.length }}) · Média: {{ averageRating }}/10
                </span>
              </h3>

              <div v-if="reviewsLoading" class="text-center text-sm text-slate-500">
                Carregando avaliações...
              </div>

              <div v-else-if="reviewsError" class="rounded-lg bg-red-50 p-3 text-sm text-red-600 dark:bg-red-900/20 dark:text-red-400">
                {{ reviewsError }}
              </div>

              <div v-else-if="!reviews.length" class="text-center text-sm text-slate-500">
                Nenhuma avaliação ainda. Seja o primeiro a avaliar!
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="review in reviews"
                  :key="review.id"
                  class="rounded-lg border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  <div class="flex items-start justify-between gap-2">
                    <div class="flex-1">
                      <p class="font-semibold text-slate-900 dark:text-white">
                        {{ review.username }}
                      </p>
                      <p class="text-xs text-slate-500 dark:text-slate-400">
                        ⭐ {{ review.rating }}/10
                      </p>
                    </div>
                    <time class="text-xs text-slate-400">
                      {{ new Date(review.created_at).toLocaleDateString('pt-BR') }}
                    </time>
                  </div>

                  <p v-if="review.comment" class="mt-2 text-sm text-slate-700 dark:text-slate-300">
                    {{ review.comment }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </Teleport>
</template>