<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'
import { fetchRecommendations } from '@/api/recommend'

const route       = useRoute()
const movieStore  = useMovieStore()

const loading     = ref(false)
const searchQuery = computed(() => route.query.q || '')
const results     = computed(() => movieStore.results)

async function fetchAndStoreResults (query) {
  loading.value = true
  try {
    const result = await fetchRecommendations(query)
    movieStore.setQuery(query)
    movieStore.setResults(result)
  } catch (error) {
    console.error('검색 추천 실패:', error)
  } finally {
    loading.value = false
  }
}

watch(
  searchQuery,
  async (newQuery) => {
    if (!newQuery) return
    await fetchAndStoreResults(newQuery)
  },
  { immediate: true }
)
</script>

<template>
  <div class="container mt-5">
    <h2 class="mb-4">🔍 검색어: "{{ searchQuery }}"</h2>

    <div v-if="loading" class="text-muted">
      GPT & TMDB에서 추천을 불러오는 중...
    </div>

    <div v-else class="row">
      <div
        class="col-md-4 mb-4"
        v-for="movie in results"
        :key="movie.id"
      >
        <router-link
          :to="`/detail/${movie.id}`"
          class="text-decoration-none text-dark"
        >
          <div class="card h-100 shadow-sm">
            <!-- ─────────── 이미지 영역 (Skeleton + 고정 비율) ─────────── -->
            <div class="img-wrapper">
              <!-- Skeleton -->
              <div class="img-skeleton"></div>

              <!-- 실제 이미지: onload 시 Skeleton 제거 -->
              <img
                v-if="movie.poster_path"
                :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
                class="w-100 h-100 object-fit-cover position-absolute top-0 start-0"
                :alt="movie.title"
                @load="e => e.target.previousElementSibling?.remove()"
              />
            </div>

            <!-- ─────────── 텍스트 영역 ─────────── -->
            <div class="card-body">
              <h5 class="card-title">{{ movie.title }}</h5>
              <p class="card-text text-muted small">
                ⭐ 평점: {{ movie.rating }}
              </p>
              <p class="card-text text-muted small">
                {{ movie.overview }}
              </p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --- Skeleton & 고정 비율 ------------------------------------------------ */
.img-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3;         /* TMDB 포스터 기본 비율 2:3 */
  overflow: hidden;
}

.img-skeleton {
  position: absolute;
  inset: 0;
  background: #e9ecef;         /* Bootstrap gray-200 */
  animation: pulse 1.6s infinite linear;
  background-size: 400% 400%;
  background-image: linear-gradient(
    -90deg,
    #e9ecef 0%,
    #f8f9fa 50%,
    #e9ecef 100%
  );
}

@keyframes pulse {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 이미지가 로드된 뒤에는 object-fit 으로 깔끔하게 맞춤 */
.object-fit-cover {
  object-fit: cover;
}
</style>
