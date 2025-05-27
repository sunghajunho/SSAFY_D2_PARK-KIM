<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <Header />
    <router-view />
  </div>
</template>

<script setup>
  import Header from '@/components/Header.vue'
// 아무 스크립트도 필요 없음
</script>