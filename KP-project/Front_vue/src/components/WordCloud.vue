<template>
  <div class="wordcloud-container">
    <h4 class="title">취향분석</h4>
    <h6 class="title">{{ description }}</h6>
    <img :src="imageUrl" alt="Wordcloud" class="wordcloud-image" />
  </div>
</template>

<script setup>
import { ref,computed,onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore' 
import api from '@/api/axios.js'

const route = useRoute()
const userStore = useUserStore()
const username = computed(() => {
  return route.params.username || userStore.username
})

// Django API의 워드클라우드 URL
const wordcloudUrl = ref(`http://localhost:8000/community/api/wordcloud/${username.value}/`)
const description = ref('')
const imageUrl = ref('')

onMounted(async () => {
  const response = await api.get(`http://127.0.0.1:8000/community/api/wordcloud/${username.value}/`)
  console.log("응답 전체:", response.data)  // ⭐️ 먼저 응답 전체 확인
  description.value = response.data.description
  imageUrl.value = `data:image/png;base64,${response.data.image}`
})

</script>

<style scoped>
.wordcloud-container {
  width: 760px;
  margin: 0 auto;
  text-align: center;
}

.wordcloud-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #ccc;
}

.title {
  margin-bottom: 10px;
}
</style>
