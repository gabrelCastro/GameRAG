<script setup>
import { useAuthStore } from '@/stores/auth'
import ChatWidget from '@/components/ChatWidget.vue'

const auth = useAuthStore()
</script>

<template>
  <main id="app" class="min-h-screen">
    <router-view />
    <ChatWidget v-if="auth.isAuthenticated" />
  </main>
</template>
