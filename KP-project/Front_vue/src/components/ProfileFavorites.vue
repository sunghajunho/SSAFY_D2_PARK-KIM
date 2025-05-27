<template>
  <div class="favorite-movies">
    <h4>찜한 영화</h4>
    <div v-if="favoriteMovies.length" class="favorite-movie-list">
      <div
        v-for="movie in favoriteMovies"
        :key="movie.id"
        class="movie-item"
        @click="goToMovieDetail(movie.id)"
      >
        <img
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :alt="movie.title"
          class="movie-poster"
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

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const favoriteMovies = ref([])

const props = defineProps({
  isMyProfile: Boolean
})

onMounted(async () => {
  await userStore.fetchFavoriteMovies(route.params.username)
  console.log(userStore.favoriteMovieIds)
  if (userStore.favoriteMovieIds.length) {
    try {
      const movieDetails = await Promise.all(
        userStore.favoriteMovieIds.map(async (id) => {
          const res = await axios.get(
            `https://api.themoviedb.org/3/movie/${id}`,
            {
              params: { api_key: 'f2fd16b8032965fdf2108baab6171e4e', language: 'ko-KR' },
            }
          )
          return res.data
          console.log(res.data)
        })
      )
      favoriteMovies.value = movieDetails
    } catch (e) {
      console.error('TMDB API 오류:', e)
      favoriteMovies.value = []  // ✅ 오류시도 안전하게 초기화!
    }
  } else {
    favoriteMovies.value = []  // ✅ 없을 때도 안전하게 초기화
  }
})

const goToMovieDetail = (movieId) => {
  router.push(`/movies/${movieId}`)
}

const removeFromFavorites = async (tmdbId) => {
  if (confirm('정말로 삭제하시겠습니까?')) {
    try {
      await axios.delete(`http://localhost:8000/accounts/favorites/remove/${tmdbId}/`, {
        headers: { Authorization: `Token ${userStore.token}` }
      })
      // 삭제 후 목록에서 제거
      favoriteMovies.value = favoriteMovies.value.filter(
        (movie) => movie.id !== tmdbId
      )
      userStore.favoriteMovieIds = userStore.favoriteMovieIds.filter(
        (id) => id !== tmdbId
      )
    } catch (e) {
      console.error('삭제 실패', e)
      alert('삭제 중 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
.favorite-movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center; /* ✅ 중앙 정렬 */
}

.movie-item {
  display:flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.movie-item:hover {
  transform: scale(1.05);
}

.movie-poster {
  width: 180px; /* ✅ 포스터 크기 조절 */
  height: 270px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.remove-btn {
  margin-top: 8px; /* 포스터 아래로 공간 */
  background: #ff4d4f;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.8rem;
  cursor: pointer;
}
</style>
