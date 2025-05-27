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
  color: var(--bs-body-color);              /* ✅ 자동 본문 색상 */
}

.wordcloud-image {
  max-width: 40%;
  aspect-ratio: 4 / 3;
  object-fit: contain;
  border: 1px solid var(--bs-border-color); /* ✅ 자동 테두리 색상 */
  display: block;
  margin: 0 auto;
  background-color: var(--bs-body-bg);      /* ✅ 이미지 배경 대비용 */
}

.title {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--bs-emphasis-color);          /* ✅ 강조 색상 자동 대응 */
  margin-bottom: 0.5rem;
  text-align: center;
  letter-spacing: 1px;
}

.description {
  font-size: 1rem;
  color: var(--bs-secondary-color);         /* ✅ 보조 텍스트 색상 */
  text-align: center;
  margin: 0 auto;
  max-width: 300px;
  line-height: 1.5;
}

</style>
