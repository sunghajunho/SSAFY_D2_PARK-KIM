<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/reviewStore'

const title = ref('')
const content = ref('')
const store = useReviewStore()
const router = useRouter()

async function submit() {
  const newID = await store.createReview({
    title: title.value,
    content: content.value
  })

  if (newID) {
    router.push(`/reviews/${newID}`)
  } else {
    alert('리뷰 작성에 실패했습니다.')
  }
}
</script>

<template>
  <div class="container mt-4">
    <h3 class="mb-3">✍️ 리뷰 작성</h3>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label class="form-label">제목</label>
        <input v-model="title" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">내용</label>
        <textarea v-model="content" class="form-control" rows="6" required />
      </div>
      <button class="btn btn-primary">등록</button>
    </form>
  </div>
</template>
