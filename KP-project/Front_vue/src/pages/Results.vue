<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'
import { fetchRecommendations } from '@/api/recommend'

const route       = useRoute()
const movieStore  = useMovieStore()

const loading     = ref(false)
const explanation = ref('')
const searchQuery = computed(() => route.query.q || '')
const model = computed(() => route.query.model || 'gpt-3.5-turbo')
const results     = computed(() => movieStore.results)

const mood = computed(() => movieStore.conditions.mood)
const situation = computed(() => movieStore.conditions.situation)
const genres = computed(() => movieStore.conditions.genres)

async function fetchAndStoreResults (query) {
  loading.value = true
  try {
    const result = await fetchRecommendations(query, model.value)
    movieStore.setQuery(query)
    movieStore.setResults(result.results || result)
    explanation.value = result.explanation || ''
  } catch (error) {
    console.error('검색 추천 실패:', error)
  } finally {
    loading.value = false
  }
}

watch(
  searchQuery,
  async (newQuery) => {
    if (!newQuery || newQuery === movieStore.query) return
    await fetchAndStoreResults(newQuery)
  },
  { immediate: true }
)
</script>

<template>
  <div class="results-container">
    <!-- 🔍 추천 결과 -->
    <h2 class="results-title">🔍 당신을 위한 추천 영화</h2>

    <!-- ✅ 로딩 애니메이션 추가 -->
    <div v-if="loading" class="loading-overlay">
      <video src="@/assets/loading_1.mp4" autoplay loop muted playsinline></video>
    </div>

    <!-- 🎯 조건 요약 영역 -->
    <div class="conditions-bar">
      <span v-if="mood" class="chip">🎭 {{ mood }}</span>
      <span v-if="situation" class="chip">🕰️ {{ situation }}</span>
      <span v-for="g in genres" :key="g" class="chip">🎬 {{ g }}</span>
    </div>

    <div v-if="loading" class="loading-overlay">
      <video src="@/assets/loading_1.mp4" autoplay loop muted playsinline></video>
    </div>

    <!-- 🧠 추천 이유 -->
    <p v-if="explanation" class="explanation-box">
      🧠 <em>{{ explanation }}</em>
    </p>
    <div v-if="loading" class="loading-msg"></div>

    <div v-else class="grid-wrapper">
      <div
        class="card"
        v-for="movie in results"
        :key="movie.id"
      >
        <router-link
          v-if="movie.id"
          :to="`/detail/${movie.id}`"
          class="card-link"
        >
          <div class="poster-wrapper">
            <img
              v-if="movie.poster_path"
              :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
              class="poster-img"
              :alt="movie.title"
            />
            <div class="overlay">
              <h5 class="title">{{ movie.title }}</h5>
              <p class="rating">⭐ {{ movie.rating || movie.vote_average?.toFixed(1) || '정보 없음' }}</p>
              <p class="reason" v-if="movie.reason">🧠 {{ movie.reason }}</p>
            </div>
          </div>
        </router-link>

        <div v-else class="card-missing">
          <h5>{{ movie.title }}</h5>
            <p>이 영화는 아직 정보가 부족합니다.</p>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.results-container {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.results-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.explanation {
  font-style: italic;
  margin-bottom: 2rem;
  color: #6c757d;
}

.loading-msg {
  color: #999;
  font-style: italic;
  margin-top: 2rem;
}

.grid-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}

.card {
  position: relative;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: transform 0.2s ease;
}
.card:hover {
  transform: scale(1.03);
}

.card-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.poster-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3;
  background-color: #eaeaea;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  opacity: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 1rem;
  transition: opacity 0.3s ease;
}

.card:hover .overlay {
  opacity: 1;
}

.object-fit-cover {
  object-fit: cover;
}

/* ✅ 로딩 애니메이션 스타일 */
.loading-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 320px; /* 필요한 만큼 높이 조절 */
}
.loading-overlay video {
  max-width: 200px;
  border-radius: 10px;
}

.overlay .title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.overlay .rating,
.overlay .reason {
  font-size: 0.85rem;
  margin-bottom: 0.2rem;
  color: #f8f9fa;
}

.card-missing {
  background-color: #f5f5f5;
  padding: 1rem;
  text-align: center;
  border-radius: 0.75rem;
  color: #999;
  font-size: 0.95rem;
}
.conditions-bar {
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.explanation-box {
  background-color: var(--bs-secondary-bg);  /* 자동 다크/라이트 대응 */
  border-left: 4px solid var(--bs-primary);
  color: var(--bs-secondary-color);
  padding: 1rem;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  margin-bottom: 2rem;
}
.chip {
  background-color: var(--bs-tertiary-bg);  /* 밝은 회색 ~ 어두운 회색 자동 전환 */
  color: var(--bs-body-color);              /* 본문 텍스트와 같은 색 */
  padding: 0.3rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 500;
}

</style>
