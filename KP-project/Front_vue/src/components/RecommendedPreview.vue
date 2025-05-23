<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'
import { fetchRecommendations } from '@/api/recommend'

const userStore = useUserStore()
const movieStore = useMovieStore()

const loading = ref(false)
const recommendations = ref([])
const showRest = ref(false)

const firstChunk = computed(() => recommendations.value.slice(0, 4))
const restChunk = computed(() => recommendations.value.slice(4))

async function loadPreviewRecommendations() {
  loading.value = true
  try {
    const prompt = userStore.isLoggedIn
      ? `${userStore.username}님의 취향에 맞는 최신 영화`
      : '요즘 인기있는 영화 추천해줘'

    const result = await fetchRecommendations(prompt)

    recommendations.value = result
    movieStore.setQuery('[홈 추천]')
    movieStore.setResults(result)

    showRest.value = false
    await nextTick()
    showRest.value = true
  } catch (e) {
    console.error('프리뷰 추천 실패:', e)
  } finally {
    loading.value = false
  }
}

onMounted(loadPreviewRecommendations)
watch(() => userStore.username, loadPreviewRecommendations)
</script>

<template>
  <div class="mt-5">
    <h5 class="mb-3">
      🎯 {{
        userStore.isLoggedIn
          ? `${userStore.username}님을 위한 추천작`
          : '요즘 핫한 영화 추천'
      }}
    </h5>

    <!-- 스켈레톤 로딩 -->
    <div v-if="loading" class="row">
      <div v-for="n in 3" :key="n" class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="skeleton-img rounded-top"></div>
          <div class="card-body">
            <div class="skeleton-text skeleton-text--wide mb-2"></div>
            <div class="skeleton-text skeleton-text--mid"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 추천 카드 -->
    <div v-else class="row">
      <!-- 먼저 보여질 4개 -->
      <router-link
        v-for="movie in firstChunk"
        :key="movie.id"
        :to="`/detail/${movie.id}`"
        class="text-decoration-none text-dark col-md-4 mb-3"
      >
        <div class="card h-100 shadow-sm">
          <img
            v-if="movie.poster_path"
            :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
            class="card-img-top preview-img"
            :alt="movie.title"
          />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text text-muted small text-truncate-2">
              {{ movie.overview }}
            </p>
          </div>
        </div>
      </router-link>

      <!-- 한 박자 뒤에 나머지 카드 -->
      <router-link
        v-if="showRest"
        v-for="movie in restChunk"
        :key="movie.id"
        :to="`/detail/${movie.id}`"
        class="text-decoration-none text-dark col-md-4 mb-3"
      >
        <div class="card h-100 shadow-sm">
          <img
            v-if="movie.poster_path"
            :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
            class="card-img-top preview-img"
            :alt="movie.title"
          />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text text-muted small text-truncate-2">
              {{ movie.overview }}
            </p>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.preview-img {
  height: 250px;
  object-fit: cover;
}
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Skeleton 스타일 */
.skeleton-img,
.skeleton-text {
  border-radius: 4px;
  animation: shimmer 2s ease-in-out infinite;
  background-size: 200% 100%;
  background-repeat: no-repeat;
}

.skeleton-img {
  height: 250px;
}
.skeleton-text--wide {
  height: 12px;
  width: 75%;
}
.skeleton-text--mid {
  height: 12px;
  width: 50%;
}

/* 라이트모드 기본 색상 */
.skeleton-img {
  background: linear-gradient(90deg, #e0e0e0 0%, #f0f0f0 50%, #e0e0e0 100%);
}
.skeleton-text {
  background: #e0e0e0;
}

/* 🌙 다크모드 */
@media (prefers-color-scheme: dark) {
  .card {
    background-color: #1f1f1f !important;
    border-color: #2a2a2a !important;
  }
  .skeleton-img,
  .skeleton-text {
    color :  #1f1f1f !important;
    background: #2a2a2a !important;
    background-image: none !important;
    animation: none !important;
  }
}

/* ✨ Shimmer 애니메이션 */
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
