<script setup>
import { onMounted,computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/reviewStore'
import { useUserStore } from '@/stores/userStore'
import CommentThread from '../components/CommentThread.vue'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()
const userStore = useUserStore()

const reviewId = parseInt(route.params.id)

const articleLikes = computed(() => reviewStore.currentReview?.article_likes ?? 0)

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

async function handleReviewLike() {
  try {
    await reviewStore.toggleReviewLike(reviewId)
  } catch (e) {
    console.error('게시글 좋아요 실패:', e)
  }
}

</script>

<template>
  <div class="container mt-4">
    <div v-if="!reviewStore.currentReview" class="text-muted">로딩 중...</div>
    <div v-else>
      <h3>글 제목: {{ reviewStore.currentReview.title }}</h3>
      <p class="m-0 text-muted small">
        작성자: 
        <router-link
          :to="reviewStore.currentReview.author.username === userStore.username ? '/profile' : `/profile/${reviewStore.currentReview.author.username}`"
          class="text-decoration-none"
        >
        {{ reviewStore.currentReview.author.username }}
        </router-link>
      </p>  
      <p class="text-muted small">조회수: {{ reviewStore.currentReview.views }}</p>
      <p>{{ reviewStore.currentReview.content }}</p>

      <div v-if="reviewStore.currentReview.author.username === userStore.username" class="mt-3">
        <!-- TODO: 수정기능 추후 구현 -->
        <button class="btn btn-sm btn-danger" @click="deleteReview">삭제</button>
      </div>
      <div>
        <button @click="handleReviewLike">
            {{ reviewStore.currentReview.is_liked ? '💔 좋아요 취소' : '❤️ 좋아요' }}
            {{ articleLikes }}
        </button>
      </div>

      <hr />
      <CommentThread :reviewId="reviewId" />
    </div>
    
    <button @click="router.push('/reviews')" class="btn btn-secondary mt-3">
      목록으로
    </button>
  </div>
</template>
