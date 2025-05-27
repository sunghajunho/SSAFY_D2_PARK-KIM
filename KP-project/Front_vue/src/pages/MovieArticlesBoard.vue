<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const movieId = route.params.id

const articles = ref([])
const loading = ref(true)

const sortOption = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10
const totalCount = ref(0)

const pageCount = computed(() => Math.ceil(totalCount.value / pageSize))

const fetchArticles = async () => {
  loading.value = true
  try {
    const { data } = await api.get(`/community/movies/${movieId}/articles/`, {
      params: {
        sort: sortOption.value,
        page: currentPage.value,
        search: searchQuery.value
      }
    })
    articles.value = data.results || data  // pagination이 없으면 data 그대로
    totalCount.value = data.count || data.length
  } catch (e) {
    console.error('게시글 목록 불러오기 실패:', e)
  } finally {
    loading.value = false
  }
}

const onSearch = () => {
  currentPage.value = 1
  fetchArticles()
}

const pageButtons = computed(() => {
  const total = pageCount.value
  const current = currentPage.value
  const delta = 2
  let start = Math.max(1, current - delta)
  let end = Math.min(total, current + delta)

  if (current <= 3) end = Math.min(total, 5)
  if (current >= total - 2) start = Math.max(1, total - 4)

  const pages = []
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const changePage = (page) => {
  if (page !== currentPage.value) {
    currentPage.value = page
    fetchArticles()
  }
}

onMounted(() => {
  fetchArticles()
})
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-3">🎬 이 영화의 모든 게시글</h2>

    <div v-if="loading" class="text-muted">게시글을 불러오는 중...</div>
    <div v-else-if="articles.length === 0" class="text-muted">아직 게시글이 없습니다.</div>

    <!-- ✅ 검색창 -->
    <div class="mb-3">
      <input
        type="text"
        v-model="searchQuery"
        @keyup.enter="onSearch"
        placeholder="게시글 내용으로 검색"
        class="form-control form-control-sm"
      />
      <button @click="onSearch" class="btn btn-sm btn-primary mt-1">검색</button>
    </div>

    <div class="mb-3 text-end">
      <select v-model="sortOption" class="form-select form-select-sm w-auto d-inline">
        <option value="">최신순</option>
        <option value="views">조회수순</option>
        <option value="likes">좋아요순</option>
      </select>
    </div>

    <!-- ✅ 게시글 리스트 -->
    <div
      v-for="article in articles"
      :key="article.id"
      class="d-flex border mb-2 align-items-center p-2"
      style="height: 80px;"
    >
      <div class="flex-grow-1">
        <p class="m-0 fw-semibold">{{ article.author.nickname || article.author.username }}</p>
        <p class="m-0 small text-muted">{{ article.content }}</p>
      </div>

      <router-link
        :to="`/reviews/${article.id}/`"
        class="btn btn-sm btn-outline-secondary ms-2"
      >
        자세히
      </router-link>
    </div>

    <!-- ✅ 페이지네이션 -->
    <div class="mt-3 text-center">
      <button
        class="btn btn-sm btn-outline-secondary me-1"
        @click="currentPage--; fetchArticles()"
        :disabled="currentPage === 1"
      >
        이전
      </button>

      <button
        v-for="page in pageButtons"
        :key="page"
        @click="changePage(page)"
        :class="['btn', 'btn-sm', page === currentPage ? 'btn-primary' : 'btn-outline-secondary', 'me-1']"
      >
        {{ page }}
      </button>

      <button
        class="btn btn-sm btn-outline-secondary"
        @click="currentPage++; fetchArticles()"
        :disabled="currentPage === pageCount"
      >
        다음
      </button>
    </div>
  </div>
</template>

<style scoped>
/* 기존 스타일 유지 */
</style>
