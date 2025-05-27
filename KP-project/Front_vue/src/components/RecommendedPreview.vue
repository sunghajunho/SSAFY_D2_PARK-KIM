<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'

const movies = ref([])
const loading = ref(true)
const error = ref('')
const router = useRouter()

const movieStore = useMovieStore()
const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const username = computed(() => userStore.username)
const favoriteGenres = computed(() => userStore.favoriteGenres || [])
const tagline = computed(() => favoriteGenres.value.slice(0, 3).join(', '))

const RECOMMEND_CACHE_TTL = 60 * 10 * 1000  // 10분

onMounted(async () => {
  const now = Date.now()
  const cached = movieStore.recommended
  const lastFetched = movieStore.recommendedAt || 0
  const isExpired = now - lastFetched > RECOMMEND_CACHE_TTL

  if (cached.length > 0 && !isExpired) {
    movies.value = cached
    loading.value = false
    return
  }

  // → 만료되었거나 없음 → 새로 불러오기
  try {
    const { data } = await api.get('api/recommend/default/?count=10')
    if (Array.isArray(data?.ids)) {
      const promises = data.ids.map(id => api.get(`api/recommend/tmdb/${id}/`).then(res => res.data))
      const result = await Promise.all(promises)
      movies.value = result
      movieStore.setRecommended(result)  // 🔄 새 캐시 저장
    } else {
      error.value = '추천 ID를 받지 못했습니다.'
    }
  } catch (e) {
    console.error(e)
    error.value = '추천을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="my-5">
    <h3 class="mb-3">
      {{ isLoggedIn ? `🎯 ${username}님의 선호 장르: ${tagline} 추천` : '🔥 요즘 사람들이 많이 보는 인기 영화' }}
    </h3>

    <!-- ✅ 로딩 애니메이션 추가 -->
    <div v-if="loading" class="loading-overlay">
      <video src="@/assets/loading_1.mp4" autoplay loop muted playsinline></video>
    </div>

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
.card-body {
  padding: 0.75rem 0.75rem 0.75rem;
}
.card-body .text-truncate {
  line-height: 1.3;
}
.card-body .small {
  line-height: 1.2;
}
.scroll-wrapper {
  padding-top: 8px;
  overflow: hidden;
  position: relative;
  width: 100%;
  height: 320px;
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
  height: 310px;
  cursor: pointer;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  background-color: #1e1e1e;
  color: #f1f1f1;
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

/* ✅ 로딩 애니메이션 스타일 */
.loading-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 320px; /* 스크롤 영역 높이와 맞춰서 */
}
.loading-overlay video {
  max-width: 200px;
  border-radius: 10px;
}
</style>

