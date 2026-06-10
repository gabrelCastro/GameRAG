<script setup>
import { computed } from 'vue'

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

const formattedPrice = computed(() => {
  const value = props.game?.price
  const number = Number(value)
  if (Number.isNaN(number)) return value ?? ''
  return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
})
</script>

<template>
  <article
    class="flex flex-col gap-4 p-6 rounded-[1.75rem] bg-white border border-slate-200 shadow-lg shadow-slate-950/10 dark:bg-slate-950 dark:border-slate-800 dark:shadow-slate-950/40"
  >
    <h2 class="text-lg font-semibold text-slate-950 dark:text-white">{{ game.title }}</h2>
    <p class="text-sm text-slate-600 dark:text-slate-400 line-clamp-4">{{ game.description }}</p>

    <div class="flex flex-col gap-3 mt-auto text-slate-500 text-xs sm:text-sm dark:text-slate-400">
      <span class="font-medium text-slate-700 dark:text-slate-300">
        {{ game.genre }}<span v-if="showPlatformBadge && game.platform"> · {{ game.platform }}</span>
      </span>
      <span v-if="showPrice" class="text-sky-500 font-semibold dark:text-sky-400">{{ formattedPrice }}</span>
    </div>
  </article>
</template>
