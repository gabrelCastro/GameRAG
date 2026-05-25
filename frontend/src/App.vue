<script setup>
import ThemeToggle from './components/ThemeToggle.vue'
</script>

<template>
  <div class="min-h-screen">
    <div class="absolute top-6 right-6 z-10">
      <ThemeToggle />
    </div>
    <router-view />
  </div>
</template>
