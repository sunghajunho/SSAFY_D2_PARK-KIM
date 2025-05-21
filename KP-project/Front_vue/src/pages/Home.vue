<script setup>
import { ref } from 'vue'
import { useThemeStore } from '@/stores/themeStore'
import RecommendedPreview from '@/components/RecommendedPreview.vue'

const query = ref('')
const themeStore = useThemeStore()

// const res = await api.post('/api/recommend/', {
//   input: null  // 또는 아예 비워둠
// })
// const recommendations = res.data.results

function search() {
  if (query.value.trim()) {
    window.location.href = `/results?q=${encodeURIComponent(query.value)}`
  }
}
</script>

<template>
  <div class="container text-center mt-5">
    <h1 class="display-4 mb-4 fw-bold">🎬 MovieGPT</h1>
    <p class="lead text-muted mb-4">GPT와 함께, 당신의 취향을 읽는 영화 추천</p>

    <div class="input-group input-group-lg mb-5 mx-auto" style="max-width: 600px;">
      <input v-model="query" class="form-control" placeholder="영화를 찾아보세요..." />
      <button class="btn btn-primary" @click="search">검색</button>
    </div>

    <RecommendedPreview />

    <div class="mt-5">
      <button class="btn btn-outline-secondary btn-sm" @click="themeStore.toggleTheme">
        🌗 테마 전환 ({{ themeStore.theme === 'light' ? '라이트' : '다크' }})
      </button>
    </div>
  </div>
</template>
