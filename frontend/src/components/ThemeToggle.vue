<script setup>
import { useThemeStore } from '@/stores/theme'

const theme = useThemeStore()
</script>

<template>
  <button
    type="button"
    aria-label="Alternar tema"
    class="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
    @click="theme.toggle"
  >
    <svg
      v-if="theme.isDark"
      class="w-6 h-6 text-yellow-500"
      fill="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        d="M12 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zM12 18a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM4.22 4.22a1 1 0 011.42 0l.7.7a1 1 0 01-1.42 1.42l-.7-.7a1 1 0 010-1.42zM17.66 17.66a1 1 0 011.42 0l.7.7a1 1 0 01-1.42 1.42l-.7-.7a1 1 0 010-1.42zM2 12a1 1 0 011-1h1a1 1 0 110 2H3a1 1 0 01-1-1zM19 12a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1zM5.64 17.66a1 1 0 010-1.42l.7-.7a1 1 0 011.42 1.42l-.7.7a1 1 0 01-1.42 0zM16.24 6.34a1 1 0 010-1.42l.7-.7a1 1 0 111.42 1.42l-.7.7a1 1 0 01-1.42 0zM12 7a5 5 0 100 10A5 5 0 0012 7z"
      />
    </svg>
    <svg v-else class="w-6 h-6 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
    </svg>
  </button>
</template>
