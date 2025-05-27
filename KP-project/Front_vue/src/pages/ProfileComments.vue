<template>
  <div>
    <h3>{{ username }}님의 댓글</h3>

    <div
      v-for="comment in store.comments"
      :key="comment.id"
      class="border p-2 mb-2"
    >
      <!-- 댓글이 작성된 게시글 정보 -->
      <div class="text-muted small mb-1">
        <router-link :to="`/reviews/${comment.article}`">
          {{ comment.article }}번 게시글
        </router-link>
      </div>

      <!-- 댓글 내용 -->
      <p class="m-0">{{ comment.content }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviewStore'

const store = useReviewStore()
const route = useRoute()
const username = route.params.username

onMounted(async () => {
  await store.fetchUserComments(username)
})
</script>
