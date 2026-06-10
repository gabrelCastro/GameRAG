<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import api from '@/services/api'

const isOpen = ref(false)
const input = ref('')
const loading = ref(false)
const messagesEl = ref(null)

const MAX_INPUT = 400

const width = ref(420)
const height = ref(560)
const MIN_W = 300
const MIN_H = 380
const MAX_W = 800

let resizing = false
let startX = 0
let startY = 0
let startW = 0
let startH = 0

function startResize(e) {
  resizing = true
  startX = e.clientX
  startY = e.clientY
  startW = width.value
  startH = height.value
  window.addEventListener('mousemove', onResize)
  window.addEventListener('mouseup', stopResize)
  e.preventDefault()
}

function onResize(e) {
  if (!resizing) return
  width.value  = Math.max(MIN_W, Math.min(MAX_W, startW + (startX - e.clientX)))
  height.value = Math.max(MIN_H, Math.min(window.innerHeight * 0.88, startH + (startY - e.clientY)))
}

function stopResize() {
  resizing = false
  window.removeEventListener('mousemove', onResize)
  window.removeEventListener('mouseup', stopResize)
}

function handleKeydown(e) {
  if (e.key === 'Escape' && isOpen.value) {
    isOpen.value = false
  }
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onBeforeUnmount(() => {
  stopResize()
  window.removeEventListener('keydown', handleKeydown)
})

const WELCOME_MESSAGE = {
  role: 'assistant',
  text: 'Olá! Sou o assistente GameRAG. Me diga o que você está procurando e vou recomendar jogos para você.',
  games: [],
  isError: false,
}

const messages = ref([{ ...WELCOME_MESSAGE }])

function toggle() {
  isOpen.value = !isOpen.value
}

function clearMessages() {
  messages.value = [{ ...WELCOME_MESSAGE }]
}

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', text, games: [], isError: false })
  input.value = ''
  loading.value = true
  await scrollToBottom()

  try {
    const { data } = await api.post('/chat/', { message: text })
    messages.value.push({ role: 'assistant', text: data.answer, games: data.games ?? [], isError: false })
  } catch (err) {
    const detail = err.response?.data?.error || 'Não foi possível obter uma resposta. Tente novamente.'
    messages.value.push({ role: 'assistant', text: detail, games: [], isError: true })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}
</script>

<template>
  <div class="fixed bottom-4 right-4 z-50 flex flex-col items-end gap-3">
    <!-- Panel -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 translate-y-4 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-4 scale-95"
    >
      <div
        v-if="isOpen"
        class="relative flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl shadow-slate-950/20 dark:border-slate-800 dark:bg-slate-950"
        :style="{ width: width + 'px', height: height + 'px' }"
      >
        <!-- Resize handle — canto superior-esquerdo -->
        <div
          class="absolute left-0 top-0 z-10 h-5 w-5 cursor-nw-resize"
          title="Arraste para redimensionar"
          @mousedown="startResize"
        >
          <!-- grip dots -->
          <svg class="h-4 w-4 text-slate-300 dark:text-slate-700" viewBox="0 0 16 16" fill="currentColor">
            <circle cx="4" cy="4" r="1.5"/>
            <circle cx="8" cy="4" r="1.5"/>
            <circle cx="4" cy="8" r="1.5"/>
            <circle cx="8" cy="8" r="1.5"/>
            <circle cx="4" cy="12" r="1.5"/>
            <circle cx="8" cy="12" r="1.5"/>
          </svg>
        </div>

        <!-- Header -->
        <div class="flex flex-shrink-0 items-center justify-between border-b border-slate-200 bg-white px-4 py-3 dark:border-slate-800 dark:bg-slate-950">
          <div class="flex items-center gap-2">
            <span class="flex h-7 w-7 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 text-xs font-bold text-white">G</span>
            <span class="text-sm font-semibold text-slate-900 dark:text-white">Assistente GameRAG</span>
          </div>
          <div class="flex items-center gap-1">
            <button
              type="button"
              aria-label="Limpar conversa"
              title="Limpar conversa"
              class="rounded-lg p-1 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-300"
              @click="clearMessages"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
            <button
              type="button"
              aria-label="Fechar chat"
              title="Fechar (Esc)"
              class="rounded-lg p-1 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-300"
              @click="toggle"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div
          ref="messagesEl"
          class="flex-1 space-y-3 overflow-y-auto px-4 py-3"
        >
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="msg.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
          >
            <div
              :class="[
                'max-w-[85%] rounded-2xl px-3 py-2 text-sm leading-relaxed',
                msg.role === 'user'
                  ? 'bg-sky-500 text-white'
                  : msg.isError
                    ? 'border border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-900 dark:bg-rose-950/30 dark:text-rose-400'
                    : 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100'
              ]"
            >
              <p class="whitespace-pre-wrap">{{ msg.text }}</p>
              <div v-if="msg.games && msg.games.length" class="mt-2 flex flex-wrap gap-1">
                <span
                  v-for="game in msg.games"
                  :key="game.id"
                  class="inline-block rounded-full bg-white/20 px-2 py-0.5 text-xs font-medium"
                >
                  {{ game.title }}
                </span>
              </div>
            </div>
          </div>

          <!-- Loading indicator -->
          <div v-if="loading" class="flex justify-start">
            <div class="rounded-2xl bg-slate-100 px-4 py-3 dark:bg-slate-800">
              <span class="flex gap-1">
                <span class="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]"></span>
                <span class="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]"></span>
                <span class="h-2 w-2 animate-bounce rounded-full bg-slate-400"></span>
              </span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="flex-shrink-0 border-t border-slate-200 bg-white px-3 pb-3 pt-2 dark:border-slate-800 dark:bg-slate-950">
          <form class="flex gap-2" @submit.prevent="send">
            <input
              v-model="input"
              type="text"
              placeholder="Pergunte sobre jogos..."
              :disabled="loading"
              :maxlength="MAX_INPUT"
              class="flex-1 rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:placeholder-slate-500"
            />
            <button
              type="submit"
              :disabled="loading || !input.trim()"
              aria-label="Enviar mensagem"
              class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-sky-500 text-white transition hover:bg-sky-400 disabled:opacity-50"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
          <p
            v-if="input.length > MAX_INPUT * 0.75"
            class="mt-1 text-right text-xs"
            :class="input.length >= MAX_INPUT ? 'text-rose-500' : 'text-slate-400'"
          >
            {{ input.length }}/{{ MAX_INPUT }}
          </p>
        </div>
      </div>
    </transition>

    <!-- Toggle button -->
    <button
      type="button"
      :aria-label="isOpen ? 'Fechar assistente' : 'Abrir assistente de jogos'"
      class="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 text-white shadow-lg shadow-indigo-500/30 transition hover:scale-105 active:scale-95"
      @click="toggle"
    >
      <svg v-if="!isOpen" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
      <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>
