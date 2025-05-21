<script setup>
import { onMounted } from 'vue'
import { useReviewStore } from '@/stores/reviewStore'
import { useRouter } from 'vue-router'

const store = useReviewStore()
const router = useRouter()

onMounted(() => {
  store.fetchReviews()
})
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-3">📝 전체 리뷰</h2>
    <div class="mb-3 text-end">
      <router-link to="/reviews/create" class="btn btn-primary btn-sm">+ 글쓰기</router-link>
    </div>
    <div v-if="store.reviews.length === 0" class="text-muted">
      등록된 리뷰가 없습니다.
    </div>
    <div v-for="review in store.reviews" :key="review.id" class="border p-3 mb-2">
      <h5>{{ review.title }}</h5>
      <p class="text-muted small">작성자: {{ review.author }}</p>
      <p>{{ review.content.slice(0, 100) }}...</p>
      <router-link :to="`/reviews/${review.id}`" class="btn btn-sm btn-outline-secondary">자세히</router-link>
    </div>
  </div>
</template>
