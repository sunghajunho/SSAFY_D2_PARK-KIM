<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const favoriteMovies = ref([])

const props = defineProps({
  isMyProfile: Boolean
})

const fetchFavoriteMovieDetails = async () => {
  try {
    // ⭐ Pinia에서 favoriteMovieIds를 채워줌
    await userStore.fetchFavoriteMovies(route.params.username)

    console.log('ID 목록:', userStore.favoriteMovieIds)  // 👈 이거 확인

    // ⭐ TMDB API로 실제 데이터 요청
    if (userStore.favoriteMovieIds.length) {
      const details = await Promise.all(
        userStore.favoriteMovieIds.map(async (id) => {
          const res = await axios.get(
            `https://api.themoviedb.org/3/movie/${id}`,
            {
              params: { api_key: 'f2fd16b8032965fdf2108baab6171e4e', language: 'ko-KR' },
            }
          )
          return res.data
        })
      )
      favoriteMovies.value = details
    } else {
      favoriteMovies.value = []
    }

    console.log('최종 데이터:', favoriteMovies.value)
  } catch (e) {
    console.error('찜한 영화 정보 로딩 실패', e)
  }
}

// ⭐ 영화 삭제 함수
const removeFromFavorites = async (tmdbId) => {
  try {
    await api.delete(`/accounts/favorites/remove/${tmdbId}/`)
    // 삭제 성공 시 목록에서 제거
    favoriteMovies.value = favoriteMovies.value.filter(
      (movie) => movie.id !== tmdbId
    )
  } catch (e) {
    console.error('찜한 영화 삭제 실패:', e)
  }
}


// ⭐️ goToMovieDetail 정의
const goToMovieDetail = (movieId) => {
  router.push(`detail/${movieId}`)
}

onMounted(fetchFavoriteMovieDetails)
</script>


<template>
  <div class="favorite-movies-container">
    <h4 class="section-title">추천 & Pick!</h4>
    <div v-if="favoriteMovies && favoriteMovies.length" class="favorite-movie-list">
      <div
        v-for="movie in favoriteMovies"
        :key="movie.id"
        class="movie-item"
      >
        <img
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :alt="movie.title"
          class="movie-poster"
          @click="goToMovieDetail(movie.id)"
        />
        <button
          v-if="isMyProfile"
          @click="removeFromFavorites(movie.id)"
          class="remove-btn"
        >
          삭제
        </button>
      </div>
    </div>
    <p v-else>찜한 영화가 없습니다.</p>
  </div>
</template>

<style scoped>
.favorite-movies-container {
  max-width: 760px;
  margin: 0 auto;
  background: var(--bs-body-bg);        /* ✅ 자동 테마 전환 */
  color: var(--bs-body-color);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--bs-border-color);
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--bs-emphasis-color);      /* 더 강조된 색상 */
  margin-bottom: 12px;
  text-align: left;
  border-bottom: 2px solid var(--bs-border-color);
  padding-bottom: 4px;
}

.favorite-movie-list {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  padding: 10px;
  gap: 16px;
}

.movie-item {
  cursor: pointer;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movie-poster {
  width: 180px;
  height: 270px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  transition: transform 0.2s ease;
}
.movie-poster:hover {
  transform: scale(1.02);
}

.remove-btn {
  margin-top: 8px;
  background: var(--bs-danger);
  color: var(--bs-light);
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.2s ease;
}
.remove-btn:hover {
  background: #c82333; /* Bootstrap red hover 대체값 */
}
</style>

