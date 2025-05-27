<script setup>
import { ref, onMounted, computed } from 'vue'
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

// ⭐️ 영화 포스터 URL
const posterUrl = ref(null)

// ⭐️ TMDB API로 영화 포스터 가져오기
const fetchPoster = async (movieTitle) => {
  const apiKey = 'f2fd16b8032965fdf2108baab6171e4e'
  const url = `https://api.themoviedb.org/3/search/movie?query=${encodeURIComponent(movieTitle)}&api_key=${apiKey}&language=ko-KR`
  try {
    const res = await fetch(url)
    const data = await res.json()
    if (data.results && data.results.length > 0) {
      const firstMovie = data.results.find(movie => movie.poster_path !== null)
      if (firstMovie) {
        return `https://image.tmdb.org/t/p/w500/${firstMovie.poster_path}`
      }
    }
  } catch (e) {
    console.error('포스터 가져오기 실패', e)
  }
  return null
}

onMounted(async () => {
  await reviewStore.fetchReview(reviewId)
  await reviewStore.fetchComments(reviewId)

  if (reviewStore.currentReview?.movie_title_display) {
    posterUrl.value = await fetchPoster(reviewStore.currentReview.movie_title_display)
  }
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
    <div v-else class="border rounded p-3 shadow-sm bg-light">
      <!-- ⭐️ 영화 포스터 + 글 정보 나란히 -->
      <div class="d-flex align-items-start mb-3">
        <!-- 포스터 (작게!) -->
        <div v-if="posterUrl" class="me-3 flex-shrink-0" style="width: 100px;">
          <img
            :src="posterUrl"
            alt="영화 포스터"
            class="img-fluid rounded"
          />
        </div>

        <!-- 글 정보 -->
        <div class="flex-grow-1">
          <h5 class="mb-1">{{ reviewStore.currentReview.title }}</h5>
          <p class="mb-1 text-muted small">
            작성자:
            <router-link
              :to="reviewStore.currentReview.author.username === userStore.username ? '/profile' : `/profile/${reviewStore.currentReview.author.username}`"
              class="text-decoration-none"
            >
              {{ reviewStore.currentReview.author.nickname }}
            </router-link>
          </p>
          <p class="mb-1 text-muted small">영화 제목:{{ reviewStore.currentReview.movie_title_display }}</p>
          <p class="mb-1 text-muted small">조회수: {{ reviewStore.currentReview.views }}</p>
        </div>
      </div>

      <!-- 글 내용 -->
      <div class="mb-2">
        <p class="mb-0">{{ reviewStore.currentReview.content }}</p>
      </div>

      <!-- 좋아요/삭제 버튼 -->
      <div class="d-flex align-items-center mb-3">
        <button @click="handleReviewLike" class="btn btn-sm btn-outline-danger me-2">
          {{ reviewStore.currentReview.is_liked ? '💔 좋아요 취소' : '❤️ 좋아요' }}
          {{ articleLikes }}
        </button>

        <button
          v-if="reviewStore.currentReview.author.username === userStore.username"
          class="btn btn-sm btn-danger"
          @click="deleteReview"
        >
          삭제
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

<style scoped>
/* ───────── 카드(본문) ───────── */
.container .border.bg-light {
  /* 부트스트랩 5.3 다크‧라이트 전환용 CSS 변수 */
  background-color: var(--bs-secondary-bg) !important;
  color:           var(--bs-body-color)    !important;
  border-color:    var(--bs-border-color)  !important;
}

/* ───────── 작은 글씨 & 보조 정보 ───────── */
.text-muted        { color: var(--bs-secondary-color) !important; }
.text-muted.small  { color: var(--bs-tertiary-color)  !important; }

/* ───────── 버튼 계열 ───────── */
.btn-outline-danger {
  color:          var(--bs-danger);
  border-color:   var(--bs-danger);
}
.btn-outline-danger:hover,
.btn-outline-danger:focus {
  background-color: var(--bs-danger-bg-subtle);
  color:            var(--bs-danger-text-emphasis);
}

.btn-danger {
  background-color: var(--bs-danger);
  border-color:     var(--bs-danger);
}
.btn-danger:hover,
.btn-danger:focus {
  background-color: var(--bs-danger-bg-subtle);
  border-color:     var(--bs-danger);
  color:            var(--bs-danger-text-emphasis);
}

/* 좋아요 숫자·아이콘이 잘 보이도록 살짝 굵게 */
.btn-outline-danger,
.btn-danger {
  font-weight: 500;
}

/* 목록으로 버튼(회색)도 테마 대응 */
.btn-secondary {
  background-color: var(--bs-secondary-bg);
  border-color:     var(--bs-border-color);
  color:            var(--bs-body-color);
}
.btn-secondary:hover,
.btn-secondary:focus {
  background-color: var(--bs-secondary-bg-hover, var(--bs-tertiary-bg));
  color:            var(--bs-body-color);
}

/* 포스터 그림자·라운드 유지하지만 어둠 테마에서도 자연스럽게 */
.img-fluid.rounded {
  box-shadow: 0 2px 6px rgba(0,0,0,.15);
}

/* 댓글 컴포넌트 내부(입력창 등)가 카드 안에서 딱 붙지 않도록 */
hr + * {
  margin-top: 1rem;
}
</style>
