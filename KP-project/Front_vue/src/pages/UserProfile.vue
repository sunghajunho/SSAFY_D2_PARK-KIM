<script setup>
import { computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useReviewStore } from '@/stores/reviewStore'

const userStore = useUserStore()
const reviewStore = useReviewStore()

// ✅ 마운트 시 리뷰/댓글 미리 가져오기
// onMounted(() => {
//   reviewStore.fetchReviews()
//   reviewStore.fetchComments()
// })

// ✅ 반응형 computed로 필터링
const myReviews = computed(() =>
  reviewStore.getReviewsByAuthor(userStore.username)
)

const myComments = computed(() =>
  reviewStore.comments.filter(c => c.author?.username === userStore.username)
)
</script>

<template>
  <div class="container mt-5">
    <h2 class="mb-3">👤 내 프로필</h2>
    <p class="text-muted">사용자명: <strong>{{ userStore.username }}</strong></p>

    <hr />

    <h4 class="mt-4">내가 쓴 리뷰</h4>
    <ul v-if="myReviews.length" class="list-group mb-4">
      <li v-for="review in myReviews" :key="review.id" class="list-group-item">
        {{ review.title }} ({{ review.createdAt }})
      </li>
    </ul>
    <p v-else class="text-muted">작성한 리뷰가 없습니다.</p>

    <h4 class="mt-4">내가 단 댓글</h4>
    <ul v-if="myComments.length" class="list-group">
      <li v-for="comment in myComments" :key="comment.id" class="list-group-item">
        {{ comment.content }} ({{ comment.createdAt }})
      </li>
    </ul>
    <p v-else class="text-muted">작성한 댓글이 없습니다.</p>
  </div>
</template>

