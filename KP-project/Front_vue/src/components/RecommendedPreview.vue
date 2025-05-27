<script setup>
import { ref, onMounted, computed, onBeforeUnmount, watch } from 'vue'
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

const fetchRecommendedMovies = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('api/recommend/default/?count=10')
    if (Array.isArray(data?.ids)) {
      const promises = data.ids.map(id => api.get(`api/recommend/tmdb/${id}/`).then(res => res.data))
      const result = await Promise.all(promises)
      movies.value = result
      movieStore.setRecommended(result)
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

onMounted(async () => {
  if (isLoggedIn.value) {
    await userStore.fetchUserInfo()
  }

  const now = Date.now()
  const cached = movieStore.recommended
  const lastFetched = movieStore.recommendedAt || 0
  const isExpired = now - lastFetched > RECOMMEND_CACHE_TTL

  if (cached.length > 0 && !isExpired) {
    movies.value = cached
    loading.value = false
    return
  }

  await fetchRecommendedMovies()
})

watch(isLoggedIn, async (newVal, oldVal) => {
  if (newVal !== oldVal) {
    movieStore.clearRecommended()
    await fetchRecommendedMovies()
  }
})

// 🎯 마우스 드래그 스크롤 제어
let isDragging = false
let startX = 0
let scrollLeft = 0
let wrapperEl = null

const startDrag = (e) => {
  isDragging = true
  wrapperEl.classList.add('dragging')
  startX = e.pageX - wrapperEl.offsetLeft
  scrollLeft = wrapperEl.scrollLeft
}

const stopDrag = () => {
  isDragging = false
  wrapperEl.classList.remove('dragging')
}

const onDrag = (e) => {
  if (!isDragging) return
  e.preventDefault()
  const x = e.pageX - wrapperEl.offsetLeft
  const walk = (x - startX) * 1.2
  wrapperEl.scrollLeft = scrollLeft - walk
}

onMounted(() => {
  wrapperEl = document.querySelector('.scroll-wrapper')
  if (!wrapperEl) return
  wrapperEl.addEventListener('mousedown', startDrag)
  wrapperEl.addEventListener('mouseleave', stopDrag)
  wrapperEl.addEventListener('mouseup', stopDrag)
  wrapperEl.addEventListener('mousemove', onDrag)
})

onBeforeUnmount(() => {
  if (!wrapperEl) return
  wrapperEl.removeEventListener('mousedown', startDrag)
  wrapperEl.removeEventListener('mouseleave', stopDrag)
  wrapperEl.removeEventListener('mouseup', stopDrag)
  wrapperEl.removeEventListener('mousemove', onDrag)
})
</script>

<template>
  <div class="my-5">
    <h3 class="mb-3 text-primary-emphasis">
      <template v-if="isLoggedIn">
        🎯 {{ username }}님의 선호 장르 기반 추천
      </template>
      <template v-else>
        🔥 당신을 위한 영화
      </template>
    </h3>
    <div v-if="isLoggedIn" class="d-flex flex-wrap gap-2 mb-3">
      <span v-for="genre in favoriteGenres" :key="genre" class="badge bg-secondary-subtle text-secondary-emphasis px-3 py-2 rounded-pill">
        🎬 {{ genre }}
      </span>
    </div>

    <div v-if="loading" class="text-muted">로딩 중...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <div v-else class="scroll-wrapper">
      <div class="scroll-track">
        <div
          v-for="movie in movies"
          :key="movie.id"
          class="scroll-card"
          @click="router.push(`/detail/${movie.id}`)"
        >
          <img
            :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
            :alt="movie.title"
            class="thumb"
          />
          <div class="card-body">
            <div class="fw-semibold text-truncate">{{ movie.title }}</div>
            <div class="text-body-secondary small">★ {{ movie.vote_average.toFixed(1) }}</div>
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
  overflow-x: auto;       /* 수평 스크롤은 유지 */
  overflow-y: visible;    /* 위로 뜨는 카드 허용 */
  position: relative;
  width: 100%;
  height: 360px;          /* 필요 시 이 값 줄여도 됨 */
  scroll-behavior: smooth;
}
.scroll-wrapper:active {
  cursor: grabbing;
}
.scroll-wrapper:hover .scroll-track {
  animation-play-state: paused;
}
.scroll-track {
  z-index: 1;
  position: relative;
  display: flex;
  gap: 1rem;
  animation: scroll-alternate 30s linear infinite alternate;
}
.scroll-card {
  flex: 0 0 auto;
  width: 180px;
  height: 310px;
  cursor: pointer;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  background-color: var(--bs-card-bg);     /* ✅ Bootstrap 자동 테마 대응 */
  color: var(--bs-body-color);             /* ✅ 텍스트도 자동 대응 */
  transition: transform 0.2s ease;
  box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.05);
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
@keyframes scroll-alternate {
  0% { transform: translateX(0); }
  50% { transform: translateX(-50%); }
  100% { transform: translateX(0); }
}
</style>
