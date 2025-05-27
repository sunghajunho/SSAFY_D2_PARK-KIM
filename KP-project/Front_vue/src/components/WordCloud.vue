<template>
  <div class="wordcloud-container">
    <h4 class="title">취향 분석</h4>
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
  max-width: 40%;         /* 조금 넓게 */
  aspect-ratio: 4 / 3;    /* 4:3 비율로 가로가 살짝 더 길게 */
  object-fit: contain;    /* 이미지가 잘리지 않도록 */
  border: 1px solid #ccc;
  display: block;
  margin: 0 auto;
}

.title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #333;            /* 짙은 회색 계열 */
  margin-bottom: 0.5rem;
  text-align: center;     /* 중앙 정렬 */
  letter-spacing: 1px;    /* 글자 간격 */
}

.description {
  font-size: 1rem;
  color: #666;            /* 중간 회색 */
  text-align: center;     /* 중앙 정렬 */
  margin: 0 auto;
  max-width: 300px;       /* 최대 폭 제한으로 가독성 ↑ */
  line-height: 1.5;       /* 줄간격 */
}
</style>
