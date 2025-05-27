<template>
  <form @submit.prevent="submit" class="mb-5">
    <!-- <div class="mb-3">
      <input v-model="movieTitle" placeholder="영화 제목 입력" />
      <button @click="searchMovie">🔍</button>
     여러 영화 검색 결과 중 선택 -->
      <!-- <ul v-if="searchResults.length">
        <li v-for="movie in searchResults" :key="movie.id" @click="selectMovie(movie)">
          {{ movie.title }} (장르: {{ movie.genres.join(', ') }})
        </li>
      </ul>

      <div v-if="selectedMovie">
        <p>선택된 영화: <strong>{{ selectedMovie.title }}</strong></p>
        <p>장르: {{ selectedMovie.genres.join(', ') }}</p>
      </div>
    </div> --> 
    <div class="dropdown-container">
      <input
        v-model="query"
        @input="onSearch"
        @keydown="onKeyDown"
        placeholder="영화 제목을 입력하세요"
        class="search-input"
      />

      <ul v-if="results.length" class="dropdown-list">
        <li
          v-for="(movie, index) in results"
          :key="movie.id"
          :class="{ highlighted: index === selectedIndex }"
          @click="selectMovie(movie)"
        >
          {{ movie.title }}
        </li>
      </ul>

      <div v-if="selectedMovie" class="selected-movie">
        🎬 선택된 영화: {{ selectedMovie.title }}
      </div>
    </div>
    <div class="mb-3">
      <label class="form-label">제목</label>
      <input v-model="title" class="form-control" required />
    </div>
    <div class="mb-3">
      <label class="form-label">내용</label>
      <textarea v-model="content" class="form-control" rows="5" required />
    </div>
    <div>
      <label for="form-label">장르</label>
      <label v-for="g in allGenres" :key="g.id">
        <input
          type="checkbox"
          :value="g.id"
          v-model="genres"
        />
        {{ g.name }}
      </label>
    </div>
    <button type="submit" class="btn btn-primary">등록</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useReviewStore } from '@/stores/reviewStore'
import { useRouter } from 'vue-router'
import axios from 'axios'

const reviewStore = useReviewStore()
const title = ref('')
const content = ref('')
const genres = ref([])
const query = ref('')
const results = ref([])
const selectedMovie = ref(null)
const selectedIndex = ref(-1)
const allGenres = ref([])

const emit = defineEmits(['submit'])


const onSearch = async () => {
  selectedIndex.value = -1
  if (query.value.trim() === '') {
    results.value = []
    return
  }

  console.log(query.value)

  try {
    const res = await axios.get(`http://localhost:8000/movies/search/`, {
      params: { title: query.value },
    })
    results.value = res.data
  } catch (error) {
    console.error('영화 검색 실패:', error)
    results.value = []
  }
}

const selectMovie = (movie) => {
  selectedMovie.value = movie
  console.log(movie.genres)
  query.value = movie.title
  results.value = []
  selectedIndex.value = -1

  if (movie.genres && movie.genres.length > 0) {
    genres.value = movie.genres.map(g => g.id)
  } else {
    genres.value = []
  }
}

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/genres/')
  allGenres.value = res.data
})

async function submit() {
  console.log('rksk',selectedMovie.value)
  const newID = await reviewStore.createReview({
    title: title.value,
    content: content.value,
    movie_title: selectedMovie.value.id,
    genre: genres.value,
  })
  console.log('서버 응답 newID:', newID)

  emit('submit', newID)

  // 폼 초기화
  title.value = ''
  content.value = ''
  genres.value = []
  query.value = ''
  selectedMovie.value = null
}
</script>