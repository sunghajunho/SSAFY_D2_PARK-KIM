<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'

const query = ref('')
const results = ref([])
const loading = ref(false)
const error = ref('')
const router = useRouter()

const suggestions = ref([])
const suggestLoading = ref(false)
const focused = ref(false)

const lastQuery = ref('')
const suggestInProgress = ref(false)

const tmdbResults = ref([])
const tmdbLoading = ref(false)
const tmdbSearched = ref(false)


let debounceTimer = null

async function search() {
  if (!query.value.trim()) return

  tmdbSearched.value = false

  suggestions.value = []
  focused.value = false

  loading.value = true
  error.value = ''
  results.value = []
  tmdbResults.value = []

  try {
    const res = await api.get('/movies/search/', { params: { title: query.value } })
    results.value = res.data || []
  } catch (e) {
    console.error(e)
    error.value = '검색 중 오류가 발생했습니다.'
  } finally {
    loading.value = false
  }
}

async function searchTMDB() {
  if (!query.value.trim()) return

  tmdbLoading.value = true
  tmdbResults.value = []

  try {
    const res = await api.get('/api/recommend/tmdb/search/', {
      params: { title: query.value }
    })

    const rawTmdb = res.data || []
    const localIds = new Set(results.value.map(m => m.id))
    tmdbResults.value = rawTmdb.filter(m => !localIds.has(m.id))
    tmdbSearched.value = true

  } catch (e) {
    console.error('TMDB 검색 실패', e)
    tmdbResults.value = []
  } finally {
    tmdbLoading.value = false
  }
}

function fetchSuggestions() {
  const trimmed = query.value.trim()
  if (trimmed === lastQuery.value) return
  lastQuery.value = trimmed

  clearTimeout(debounceTimer)

  if (trimmed.length < 2) {
    suggestions.value = []
    return
  }

  if (trimmed.length === 2 || suggestions.value.length === 0) {
    getSuggestionsNow()
  } else {
    debounceTimer = setTimeout(() => {
      getSuggestionsNow()
    }, 150)
  }
}

async function getSuggestionsNow() {
  if (suggestInProgress.value) return
  suggestInProgress.value = true
  suggestLoading.value = true

  try {
    const res = await api.get('/movies/suggest/', {
      params: { q: query.value.trim() }
    })
    suggestions.value = (res.data || []).slice(0, 4)
  } catch (e) {
    console.error('자동완성 실패', e)
  } finally {
    suggestLoading.value = false
    suggestInProgress.value = false
  }
}

function goToDetail(id) {
  suggestions.value = []
  router.push(`/detail/${id}`)
}

function onBlur() {
  setTimeout(() => {
    focused.value = false
  }, 200)
}
</script>

<template>
  <section class="container my-4">
    <h2 class="mb-4">🔍 영화 검색</h2>

    <div class="input-group mb-3 position-relative" style="max-width: 600px;">
      <input
        v-model="query"
        @input="fetchSuggestions"
        @keyup.enter="search"
        @focus="focused = true"
        @blur="onBlur"
        class="form-control"
        placeholder="영화 제목을 입력하세요"
      />
      <button class="btn btn-primary" @click="search">검색</button>

      <ul
        v-if="suggestions.length > 0 && focused"
        class="list-group position-absolute w-100 zindex-dropdown"
        style="top: 100%; left: 0; max-height: 300px; overflow-y: auto;"
      >
        <li
          v-for="s in suggestions"
          :key="s.id"
          class="list-group-item list-group-item-action"
          @click="goToDetail(s.id)"
          style="cursor: pointer"
        >
          {{ s.title }}
        </li>
        <li v-if="suggestLoading" class="list-group-item disabled text-muted">
          <span class="spinner-border spinner-border-sm me-2" /> 불러오는 중...
        </li>
      </ul>
    </div>

    <div v-if="loading">검색 중...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <!-- 🔍 로컬 결과 -->
    <div v-else-if="results.length > 0 && !loading" class="row loaded-fade">
      <div
        v-for="movie in results"
        :key="movie.id"
        class="col-md-3 mb-4"
        @click="goToDetail(movie.id)"
        style="cursor: pointer"
      >
        <div class="card h-100 shadow-sm">
          <img
            v-if="movie.poster_path"
            :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
            :alt="movie.title"
            class="card-img-top"
          />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text text-muted small">{{ movie.overview?.slice(0, 80) }}...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 🔘 TMDB 검색 트리거 버튼 -->
    <div v-if="results.length > 0 && !loading && !tmdbSearched" class="text-center mt-3">
      <button class="btn btn-outline-secondary btn-sm" @click="searchTMDB" :disabled="tmdbLoading">
        <span v-if="tmdbLoading" class="spinner-border spinner-border-sm me-2" />
        🔎 찾으시는 영화가 없으신가요?
      </button>
    </div>

    <!-- 🔧 TMDB 결과 -->
    <div v-if="tmdbResults.length > 0 && !tmdbLoading" class="mt-5 loaded-fade">
      <h4 class="mb-3">혹시 이 영화를 찾으셨나요?</h4>
      <div class="row">
        <div
          v-for="movie in tmdbResults"
          :key="movie.id"
          class="col-md-3 mb-4"
          @click="goToDetail(movie.id)"
          style="cursor: pointer"
        >
          <div class="card h-100 shadow-sm border-warning">
            <img
              v-if="movie.poster_path"
              :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
              :alt="movie.title"
              class="card-img-top"
            />
            <div class="card-body">
              <h5 class="card-title">{{ movie.title }}</h5>
              <p class="card-text text-muted small">{{ movie.overview?.slice(0, 80) }}...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.card {
  transition: transform 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
}
.zindex-dropdown {
  z-index: 1050;
}
.list-group {
  border-radius: 0 0 0.5rem 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.loaded-fade {
  animation: fadeInUp 0.4s ease both;
  will-change: transform, opacity;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
