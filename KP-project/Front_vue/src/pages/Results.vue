<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchRecommendations } from '@/api/gpt'
import { searchMovieByTitle } from '@/api/tmdb'
import { createPrompt } from '@/utils/prompt'
import { useMovieStore } from '@/stores/movieStore'

const loading = ref(false)
const route = useRoute()
const movieStore = useMovieStore()

const searchQuery = computed(() => route.query.q || '')
const results = computed(() => movieStore.results)

async function fetchAndEnrichResults(query) {
  loading.value = true
  try {
    const prompt = createPrompt(query)
    const raw = await fetchRecommendations(prompt)
    const parsed = JSON.parse(raw)

    const gptResult = Array.isArray(parsed)
      ? parsed
      : parsed.recommendations || []

    if (!Array.isArray(gptResult)) {
      throw new Error('GPT 응답 형식이 올바르지 않습니다.')
    }

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

    movieStore.setQuery(query)
    movieStore.setResults(enrichedResults)
  } catch (error) {
    console.error('추천 데이터 처리 중 에러 발생:', error)
  } finally {
    loading.value = false
  }
}

watch(
  searchQuery,
  async (newQuery) => {
    if (!newQuery) return
    if (
      movieStore.query.trim().toLowerCase() === newQuery.trim().toLowerCase() &&
      results.value.length > 0
    ) {
      console.log('[Pinia] 캐시된 결과 사용')
      return
    }

    await fetchAndEnrichResults(newQuery)
  },
  { immediate: true }
)
</script>


<template>
  <div class="container mt-5">
    <h2 class="mb-4">🔍 검색어: "{{ searchQuery }}"</h2>

    <div v-if="loading" class="text-muted">GPT & TMDB에서 추천을 불러오는 중...</div>

    <div v-else class="row">
      <div
        class="col-md-4 mb-4"
        v-for="(movie, i) in results"
        :key="i"
      >
        <router-link
          :to="`/detail/${movie.id}`"
          class="text-decoration-none text-dark"
        >
          <div class="card h-100 shadow-sm">
            <img
              v-if="movie.poster"
              :src="movie.poster"
              class="card-img-top"
              :alt="movie.title"
            />
            <div class="card-body">
              <h5 class="card-title">{{ movie.title }}</h5>
              <p class="card-text">{{ movie.description }}</p>
              <p class="card-text text-muted small">⭐ 평점: {{ movie.rating }}</p>
              <p class="card-text text-muted small">{{ movie.overview }}</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>
