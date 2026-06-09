<template>
  <header class="flex items-center justify-between px-5 py-4 bg-white text-slate-900 border-b border-gray-200 dark:bg-slate-950 dark:text-slate-100 dark:border-gray-800">
    <div class="flex items-center">
      <h1 class="text-xl font-bold">GameRAG</h1>
    </div>

    <div class="flex items-center gap-3">
      <ThemeToggle class="inline-flex" />

      <button
        class="inline-flex items-center gap-3 px-3 py-2 rounded-full bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 transition hover:bg-slate-200 dark:hover:bg-slate-700"
        type="button"
        @click="onProfileClick"
      >
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-indigo-600 text-white font-semibold">
          {{ initials }}
        </span>
        <span class="text-sm font-medium">{{ displayName }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import ThemeToggle from './ThemeToggle.vue'

const props = defineProps({
  username: {
    type: String,
    default: 'Usuário'
  }
})

const emit = defineEmits(['profile-click'])

const displayName = computed(() => props.username || 'Usuário')

const initials = computed(() => {
  return displayName.value
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0].toUpperCase())
    .join('')
})

const onProfileClick = () => {
  emit('profile-click')
}
</script>
