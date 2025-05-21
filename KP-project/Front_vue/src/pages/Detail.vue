<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getMovieDetails } from '@/api/tmdb'
import { useMovieStore } from '@/stores/movieStore'

// Pinia store
const movieStore = useMovieStore()
const route = useRoute()

const movie = ref(null)
const loading = ref(true)

async function fetchMovie() {
  loading.value = true
  try {
    const data = await getMovieDetails(route.params.id)
    movie.value = data
  } catch (e) {
    console.error('영화 정보를 불러오는데 실패함:', e)
  }
  loading.value = false
}

// 최초 진입 시
onMounted(fetchMovie)

// 라우트가 바뀔 때도 다시 요청 (ex: 다른 영화 상세 클릭 시)
watch(() => route.params.id, fetchMovie)
</script>


<template>
  <div class="container mt-5 mb-5">
    <div v-if="loading" class="text-center text-muted">영화 정보를 불러오는 중...</div>

    <div v-else class="row">
      <div class="col-md-4 mb-4">
        <img
          v-if="movie.poster_path"
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :alt="movie.title"
          class="img-fluid rounded shadow-sm"
        />
      </div>

      <div class="col-md-8">
        <h2 class="mb-2">{{ movie.title }}</h2>
        <p class="text-muted fst-italic" v-if="movie.tagline">{{ movie.tagline }}</p>
        <p class="lead">{{ movie.overview }}</p>

        <ul class="list-unstyled small text-muted mt-4">
          <li>⭐ <strong>평점:</strong> {{ movie.vote_average }}</li>
          <li>⏱️ <strong>상영시간:</strong> {{ movie.runtime }}분</li>
          <li>🎭 <strong>장르:</strong> {{ movie.genres.map(g => g.name).join(', ') }}</li>
          <li>
            🎬 <strong>감독:</strong>
            {{ (movie.credits.crew.find(p => p.job === 'Director') || {}).name || '정보 없음' }}
          </li>
          <li>
            👥 <strong>출연:</strong>
            {{ movie.credits.cast.slice(0, 5).map(a => a.name).join(', ') }}
          </li>
        </ul>

        <router-link
          :to="{ name: 'Results', query: { q: movieStore.query } }"
          class="btn btn-outline-primary mt-4"
        >
          ← 추천 결과로 돌아가기
        </router-link>


      </div>
    </div>
  </div>
</template>
