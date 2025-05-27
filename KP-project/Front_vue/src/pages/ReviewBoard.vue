<script setup>
import { ref,onMounted,watch,computed } from 'vue'
import { useReviewStore } from '@/stores/reviewStore'
import { useRouter,RouterLink } from 'vue-router'

const store = useReviewStore()
const router = useRouter()

const sortOption = ref('')

const currentPage = ref(1)
const searchQuery = ref('')
const pageSize = 10

const pageCount = computed(() => Math.ceil(store.totalCount / 10))

const fetchReviews = () => {
  store.fetchReviews(sortOption.value, currentPage.value, searchQuery.value) // ✅ 선택된 기준으로 fetch
}

const onSearch = () => {
  currentPage.value = 1
  fetchReviews()
}

// ✅ 정렬 기준이 바뀔 때마다 자동으로 다시 불러오기
watch(sortOption, () => {
  currentPage.value = 1
  fetchReviews()
})

onMounted(() => {
  fetchReviews()
})

// 페이지 버튼 리스트 (ex: [1, 2, 3, 4, 5])
const pageButtons = computed(() => {
  const total = pageCount.value
  const current = currentPage.value
  const delta = 2
  let start = Math.max(1, current - delta)
  let end = Math.min(total, current + delta)

  // 항상 5개 버튼 보장
  if (current <= 3) {
    end = Math.min(total, 5)
  }
  if (current >= total - 2) {
    start = Math.max(1, total - 4)
  }

  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const changePage = (page) => {
  if (page !== currentPage.value) {
    currentPage.value = page
    fetchReviews()
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-3">📝 전체 리뷰</h2>
    <div class="mb-3 text-end">
      <router-link :to="{ name: 'ReviewWrite'}" class="btn btn-primary btn-sm">+ 글쓰기</router-link>
    </div>
    <div v-if="store.reviews.length === 0" class="text-muted">
      등록된 리뷰가 없습니다.
    </div>

    <!-- ✅ 검색창 -->
    <div class="mb-3">
      <input
        type="text"
        v-model="searchQuery"
        @keyup.enter="onSearch"
        placeholder="영화 제목 또는 장르로 검색"
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
    
    <div
      v-for="review in store.reviews"
      :key="review.id"
      class="d-flex border mb-2 align-items-center p-2"
      style="height: 80px;"
    >
      <!-- 텍스트 영역 -->
      <div class="flex-grow-1">
        <h6 class="m-0">{{ review.title }}</h6>
        <p class="m-0 text-muted small">{{ review.author.nickname }}</p>
        <p class="text-muted small">영화 제목: {{ review.movie_title_display }}</p>
      </div>

      <!-- 자세히 버튼 -->
      <router-link
        :to="`/reviews/${review.id}`"
        class="btn btn-sm btn-outline-secondary"
        style="margin-left: 10px;"
      >
        자세히
      </router-link>
    </div>

    <!-- 페이지네이션 -->
    <div class="mt-3 text-center">
      <button
        class="btn btn-sm btn-outline-secondary me-1"
        @click="currentPage--; fetchReviews()"
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
        @click="currentPage++; fetchReviews()"
        :disabled="currentPage === pageCount"
      >
        다음
      </button>
    </div>
  </div>
</template>

