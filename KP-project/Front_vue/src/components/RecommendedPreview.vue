<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const movies = ref([])
const loading = ref(true)
const error = ref('')
const router = useRouter()

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const username = computed(() => userStore.username)
const favoriteGenres = computed(() => userStore.favoriteGenres || [])
const tagline = computed(() => favoriteGenres.value.slice(0, 3).join(', '))

async function fetchRecommendations() {
  try {
    const { data } = await api.get('api/recommend/default/?count=10')
    if (Array.isArray(data?.ids)) {
      const promises = data.ids.map(id => api.get(`api/recommend/tmdb/${id}/`).then(res => res.data))
      movies.value = await Promise.all(promises)
    } else {
      error.value = '추천 ID를 받지 못했습니다.'
    }
  } catch (e) {
    console.error(e)
    error.value = '추천을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchRecommendations)
</script>

<template>
  <div class="my-5">
    <h3 class="mb-3">
      {{ isLoggedIn ? `🎯 ${username}님의 선호 장르: ${tagline} 추천` : '🔥 요즘 사람들이 많이 보는 인기 영화' }}
    </h3>

    <div v-if="loading" class="text-muted">로딩 중...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <div v-else class="scroll-wrapper">
      <div class="scroll-track">
        <div v-for="movie in movies" :key="movie.id" class="scroll-card" @click="router.push(`/detail/${movie.id}`)">
          <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" :alt="movie.title" class="thumb" />
          <div class="card-body">
            <div class="fw-semibold text-truncate">{{ movie.title }}</div>
            <div class="text-muted small">★ {{ movie.vote_average.toFixed(1) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scroll-wrapper {
  overflow: hidden;
  position: relative;
  width: 100%;
  height: 280px;
}
.scroll-track {
  display: flex;
  gap: 1rem;
  animation: scroll-left 30s linear infinite;
}
.scroll-wrapper:hover .scroll-track {
  animation-play-state: paused;
}
.scroll-card {
  flex: 0 0 auto;
  width: 180px;
  cursor: pointer;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  background: #fff;
  transition: transform 0.2s ease;
}
.scroll-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.scroll-card .thumb {
  width: 100%;
  height: 240px;
  object-fit: cover;
}
@keyframes scroll-left {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}
</style>
