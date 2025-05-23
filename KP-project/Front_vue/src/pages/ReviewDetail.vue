<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/reviewStore'
import { useUserStore } from '@/stores/userStore'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()
const userStore = useUserStore()

const reviewId = parseInt(route.params.id)

onMounted(async () => {
  await reviewStore.fetchReview(reviewId)
  await reviewStore.fetchComments(reviewId)
})

async function deleteReview() {
  if (confirm('리뷰를 삭제하시겠습니까?')) {
    await reviewStore.deleteReview(reviewId)
    router.push('/reviews')
  }
}
</script>

<template>
  <div class="container mt-4">
    <div v-if="!reviewStore.currentReview" class="text-muted">로딩 중...</div>
    <div v-else>
      <h3>{{ reviewStore.currentReview.title }}</h3>
      <p class="text-muted small">작성자: {{ reviewStore.currentReview.author.nickname }}</p>
      <p>{{ reviewStore.currentReview.content }}</p>

      <div v-if="reviewStore.currentReview.author.username === userStore.username" class="mt-3">
        <!-- TODO: 수정기능 추후 구현 -->
        <button class="btn btn-sm btn-danger" @click="deleteReview">삭제</button>
      </div>

      <hr />
      <CommentThread :reviewId="reviewId" />
    </div>
  </div>
</template>
