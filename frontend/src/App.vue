<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
import Header from './components/Header.vue'
</script>

<template>
  <div class="container">
    <Header />
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped>

</style>
