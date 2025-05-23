<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

/* ───── 상태 ─────────────────────────── */
const route   = useRoute()
const movie   = ref(null)
const error   = ref('')
const loading = ref(true)

/* ───── 데이터 fetch ─────────────────── */
async function fetchMovie () {
  try {
    const id = route.params.id
    const { data } = await api.get(`api/recommend/tmdb/${id}/`)
    movie.value = data
  } catch (err) {
    console.error(err)
    error.value = '영화 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}
onMounted(fetchMovie)

/* ───── 계산 속성 ─────────────────────── */
const director = computed(() =>
  movie.value?.credits?.crew?.find((c) => c.job === 'Director')
)
const castCards = computed(() => {
  const cards = []
  if (director.value) {
    cards.push({
      id:   director.value.id,
      name: director.value.name,
      role: '감독',
      profile: director.value.profile_path,
    })
  }
  movie.value?.credits?.cast?.slice(0, 10)?.forEach((c) =>
    cards.push({
      id:   c.id,
      name: c.name,
      role: c.character || '출연',
      profile: c.profile_path,
    })
  )
  return cards
})

/* ───── 캐러셀 스크롤 핸들러 ───────────── */
function scrollByPx (px) {
  const bar = document.querySelector('.cast-scroll')
  bar?.scrollBy({ left: px, behavior: 'smooth' })
}
</script>

<template>
  <section class="container my-4">
    <!-- 로딩 -->
    <div v-if="loading" class="text-center py-5">
      <span class="spinner-border" role="status" aria-hidden="true" />
      <p class="mt-3">불러오는 중…</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <!-- 정상 -->
    <div v-else class="row">
      <!-- ───── 왼쪽: 포스터 ───── -->
      <div class="col-md-4 text-center mb-3">
        <img
          v-if="movie.poster_path"
          :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
          :alt="movie.title"
          class="img-fluid rounded shadow"
        />
        <div v-else class="bg-secondary text-white p-5 rounded">포스터 없음</div>
      </div>

      <!-- ───── 오른쪽: 정보 ───── -->
      <div class="col-md-8">
        <h2 class="fw-bold">{{ movie.title }}</h2>
        <p class="text-muted mb-1">
          평점 ★ {{ movie.vote_average?.toFixed(1) ?? 'N/A' }}
        </p>
        <p>{{ movie.overview || '줄거리 정보가 없습니다.' }}</p>

        <!-- 장르 -->
        <div v-if="movie.genres?.length">
          <h5 class="mt-4">장르</h5>
          <span v-for="g in movie.genres" :key="g.id" class="badge bg-primary me-2">
            {{ g.name }}
          </span>
        </div>

        <!-- 개봉일 -->
        <div v-if="movie.release_date" class="mt-3">
          <small class="text-muted">개봉일: {{ movie.release_date }}</small>
        </div>
      </div>

      <!-- ───── 썸네일 캐스팅 캐러셀 ───── -->
      <div v-if="castCards.length" class="col-12 mt-5 position-relative">
        <h4 class="mb-3">감독/출연</h4>

        <!-- 좌우 스크롤 버튼 -->
        <button
          class="carousel-btn start-0"
          @click="scrollByPx(-300)"
          aria-label="왼쪽으로"
        >
          ‹
        </button>
        <button
          class="carousel-btn end-0"
          @click="scrollByPx(300)"
          aria-label="오른쪽으로"
        >
          ›
        </button>

        <div
          class="cast-scroll d-flex gap-3 overflow-auto pb-2"
          tabindex="0"
          @keydown.left.prevent="scrollByPx(-300)"
          @keydown.right.prevent="scrollByPx(300)"
        >
          <div
            v-for="person in castCards"
            :key="person.id"
            class="text-center flex-shrink-0"
            style="width: 110px"
          >
            <!-- 페이드-인 적용 -->
            <transition name="fade" appear>
              <img
                v-if="person.profile"
                :src="'https://image.tmdb.org/t/p/w185' + person.profile"
                class="rounded-circle cast-photo mb-2"
                :alt="person.name"
                loading="lazy"
              />
              <div
                v-else
                class="rounded-circle bg-secondary d-flex align-items-center justify-content-center text-white mb-2"
                style="width: 100px; height: 100px"
              >
                <i class="bi bi-person fs-2" />
              </div>
            </transition>

            <div class="small fw-semibold text-truncate">{{ person.name }}</div>
            <div class="small text-muted text-truncate">{{ person.role }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
img { max-height: 540px; object-fit: cover; }

.cast-photo { width: 100px; height: 100px; object-fit: cover; }

/* 페이드-인 */
.fade-enter-from, .fade-leave-to { opacity: 0; transform: scale(0.95); }
.fade-enter-active, .fade-leave-active { transition: opacity .4s ease, transform .4s ease; }

/* 캐러셀 스크롤바 */
.cast-scroll::-webkit-scrollbar { height: 6px; }
.cast-scroll::-webkit-scrollbar-thumb { background-color: #ced4da; border-radius: 3px; }

/* 좌·우 버튼 */
.carousel-btn {
  position: absolute;
  top: 50%;
  translate: 0 -50%;
  z-index: 1;
  border: none;
  background: rgba(255,255,255,.8);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 20px;
  line-height: 20px;
  padding: 0;
  color: #495057;
  box-shadow: 0 0 4px rgba(0,0,0,.15);
}
.carousel-btn:hover { background: #f1f3f5; }
.carousel-btn:focus { outline: none; box-shadow: 0 0 0 3px rgba(0,123,255,.25); }
</style>
