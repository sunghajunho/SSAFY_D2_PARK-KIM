<template>
  <form @submit.prevent="handleSubmit" class="mb-5">
    <div class="mb-3">
      <label class="form-label">제목</label>
      <input v-model="title" class="form-control" required />
    </div>
    <div class="mb-3">
      <label class="form-label">내용</label>
      <textarea v-model="content" class="form-control" rows="5" required />
    </div>
    <div class="mb-3">
      <label class="form-label">작성자</label>
      <input v-model="author" class="form-control" placeholder="익명" />
    </div>
    <button type="submit" class="btn btn-primary">등록</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useReviewStore } from '@/stores/reviewStore'
import { useUserStore } from '@/stores/userStore'

const reviewStore = useReviewStore()
const title = ref('')
const content = ref('')
const author = ref('')
const userStore = useUserStore()

function handleSubmit() {
  reviewStore.addReview({ title: title.value, content: content.value, author: userStore.username })
  title.value = ''
  content.value = ''
  author.value = ''
}
</script>
