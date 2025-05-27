<template>
  <div>
    <h3>{{ username }}님의 게시글</h3>

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
        <p class="text-muted small">조회수: {{ review.views }}</p>
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
  await store.fetchUserReviews(username)
})
</script>
