<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'
import { fetchRecommendations } from '@/api/gpt'
import { searchMovieByTitle } from '@/api/tmdb'
import { createHomePrompt } from '@/utils/prompt'
import { getWithExpiry, setWithExpiry } from '@/utils/cache'

const userStore = useUserStore()
const movieStore = useMovieStore()

const loading = ref(false)
const recommendations = ref([])

const results = computed(() => movieStore.results)

const cacheKey = computed(() =>
  userStore.isLoggedIn
    ? `home_recommend_${userStore.username}`
    : 'home_recommend_guest'
)

async function fetchAndEnrichRecommendations(forceRefresh = false) {
  loading.value = true

  const cached = getWithExpiry(cacheKey.value)
  if (!forceRefresh && cached) {
    recommendations.value = cached
    movieStore.setQuery('[홈 추천]')
    movieStore.setResults(cached)
    loading.value = false
    return
  }

  try {
    const prompt = createHomePrompt(userStore.isLoggedIn ? userStore.username : null)
    const raw = await fetchRecommendations(prompt)
    const parsed = JSON.parse(raw)

    const gptResult = Array.isArray(parsed)
      ? parsed
      : parsed.recommendations || []

    const enrichedResults = (
      await Promise.all(
        gptResult.map(async (item) => {
          const tmdb = await searchMovieByTitle(item.title)
          if (!tmdb || !tmdb.id) {
            console.warn(`[TMDB 검색 실패] ${item.title}`)
            return null
          }

          return {
            ...item,
            id: tmdb.id,
            poster: tmdb.poster_path
              ? `https://image.tmdb.org/t/p/w500${tmdb.poster_path}`
              : null,
            overview: tmdb.overview || '',
            rating: tmdb.vote_average || 'N/A',
          }
        })
      )
    ).filter(Boolean)

    movieStore.setQuery('[홈 추천]')
    movieStore.setResults(enrichedResults)
    recommendations.value = enrichedResults
    setWithExpiry(cacheKey.value, enrichedResults, 1000 * 60 * 60 * 6)
  } catch (error) {
    console.error('에러 발생:', error)
    recommendations.value = []
    movieStore.setResults([])
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAndEnrichRecommendations()
})

watch(
  () => userStore.username,
  () => {
    console.log('[유저 변경 감지] 캐시 초기화 및 추천 재요청')
    fetchAndEnrichRecommendations(true)
  }
)
</script>

<template>
  <div class="mt-5">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="mb-0">
        🎯 {{ userStore.isLoggedIn ? `${userStore.username}님을 위한 추천작` : '요즘 핫한 영화 추천' }}
      </h5>
      <button class="btn btn-sm btn-outline-primary" @click="fetchAndEnrichRecommendations(true)">
        🔄 새로 추천받기
      </button>
    </div>

    <div v-if="loading" class="text-muted">영화 로딩 중...</div>
    <div v-else-if="results.length === 0" class="text-muted">추천 결과가 없습니다.</div>

    <div class="row">
      <div
        v-for="(movie, i) in results"
        :key="i"
        class="col-12 col-sm-6 col-md-4 mb-4"
      >
        <router-link
          :to="`/detail/${movie.id}`"
          class="text-decoration-none text-dark h-100 d-block"
        >
          <div class="card h-100 shadow-sm">
            <img
              v-if="movie.poster"
              :src="movie.poster"
              class="card-img-top preview-img"
              :alt="movie.title"
            />
            <div class="card-body">
              <h6 class="card-title mb-1">{{ movie.title }}</h6>
              <p class="card-text text-muted small text-truncate-2">{{ movie.overview }}</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card:hover {
  transform: translateY(-2px);
  transition: all 0.2s ease;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.preview-img {
  height: 200px;
  object-fit: cover;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>