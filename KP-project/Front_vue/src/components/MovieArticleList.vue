<template>
  <div class="mt-5">
    <h4 class="d-flex align-items-center">
      유저들의 리뷰 💬
      <a
        v-if="articles.length > 0"
        @click.prevent="goToAllArticles"
        href="#"
        class="ms-auto text-decoration-none small"
      >
        더보기 &gt;
      </a>
    </h4>

    <div v-if="loading" class="text-muted">게시글을 불러오는 중...</div>
    <div v-else-if="articles.length === 0" class="text-muted">아직 게시글이 없습니다.</div>

    <div v-else class="row">
      <div
        v-for="article in articles"
        :key="article.id"
        class="col-md-4 mb-4"
      >
        <router-link
          :to="`/reviews/${article.id}/`"
          class="text-decoration-none text-dark"
        >
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <img
                  :src="article.author.profile_image"
                  class="rounded-circle me-2"
                  width="32"
                  height="32"
                />
                <strong>{{ article.author.nickname || article.author.username }}</strong>
              </div>
              <p class="small">{{ article.content }}</p>
            </div>
            <div class="card-footer bg-transparent border-0 d-flex justify-content-between">
              <small class="text-muted">{{ new Date(article.created_at).toLocaleDateString() }}</small>
              <div>
                <small class="text-muted me-2">💬 {{ article.comments.length }}</small>
                <small class="text-muted">👍 {{ article.article_likes }}</small>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const movieId = route.params.id

const articles = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get(`/community/movies/${movieId}/articles/`)
    articles.value = data
  } catch (e) {
    console.error('게시글 불러오기 실패:', e)
  } finally {
    loading.value = false
  }
})

const goToAllArticles = () => {
  router.push(`/movies/${movieId}/articles`)  // 예: /movies/1/articles
}
</script>

<style scoped>
.card {
  transition: transform 0.2s ease;
}
.card:hover {
  transform: translateY(-3px);
}
</style>

