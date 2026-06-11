<template>
  <header
    role="banner"
    class="w-full flex items-center justify-between px-4 py-3 bg-white text-slate-900 border-b border-gray-200 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-800 sm:px-5"
  >
    <!-- Logo -->
    <button
      type="button"
      @click="selectMenu('pesquisa')"
      class="flex items-center gap-2 shrink-0"
    >
      <h1 class="text-xl font-semibold">GameRAG</h1>
    </button>

    <!-- Ações -->
    <div class="flex items-center gap-2 sm:gap-3">
      <ThemeToggle class="inline-flex shrink-0" />

      <div class="relative">
        <button
          class="inline-flex items-center gap-2 px-2 py-1.5 sm:px-3 sm:py-2 rounded-full bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 transition hover:bg-slate-200 dark:hover:bg-slate-700"
          type="button"
          @click.stop="toggleMenu"
          :aria-expanded="showMenu"
          aria-haspopup="menu"
          aria-label="Abrir menu de usuário"
        >
          <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-indigo-600 text-white font-semibold shrink-0">
            {{ initials }}
          </span>
          <span class="hidden sm:inline text-sm font-medium truncate max-w-[8rem]">{{ displayName }}</span>
        </button>

        <div
          v-if="showMenu"
          role="menu"
          aria-label="Opções de usuário"
          class="absolute right-0 mt-2 w-44 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-lg shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-950 z-10"
        >
          <button
            type="button"
            role="menuitem"
            class="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-100 dark:hover:bg-slate-800"
            @click="selectMenu('profile')"
          >
            Perfil
          </button>
          <button
            type="button"
            role="menuitem"
            class="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-100 dark:hover:bg-slate-800"
            @click="selectMenu('settings')"
          >
            Configurações
          </button>
          <button
            type="button"
            role="menuitem"
            class="w-full px-4 py-3 text-left text-sm text-red-600 hover:bg-slate-100 dark:text-red-500 dark:hover:bg-slate-800"
            @click="selectMenu('logout')"
          >
            Sair
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import ThemeToggle from './ThemeToggle.vue'

const props = defineProps({
  username: {
    type: String,
    default: 'Usuário'
  }
})

const emit = defineEmits(['profile-click', 'settings-click', 'logout', 'pesquisa'])

const showMenu = ref(false)

const displayName = computed(() => props.username || 'Usuário')

const initials = computed(() => {
  return displayName.value
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0].toUpperCase())
    .join('')
})

function toggleMenu() {
  showMenu.value = !showMenu.value
}

function selectMenu(action) {
  showMenu.value = false
  if (action === 'profile') emit('profile-click')
  if (action === 'settings') emit('settings-click')
  if (action === 'logout') emit('logout')
  if (action === 'pesquisa') emit('pesquisa')
}
</script>
