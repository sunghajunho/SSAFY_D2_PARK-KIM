<template>
  <div class="container mt-5">
    <h2>✍️ 리뷰 작성</h2>
    <ReviewCreate @submit="handleSubmit" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import ReviewCreate from '../components/ReviewCreate.vue'

const router = useRouter()

function handleSubmit(newID) {
  console.log('newId:',newID)
  if (newID) {
    router.push(`/reviews/${newID}`)
  } else {
    alert('리뷰 작성에 실패했습니다.')
  }
}
</script>
