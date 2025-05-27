<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'
import { useMovieStore } from '@/stores/movieStore'
import MovieArticleList from '@/components/MovieArticleList.vue'

/* ───────────────────────── 상태 ───────────────────────── */
const route         = useRoute()
const movie         = ref(null)
const loading       = ref(true)
const error         = ref('')

/* 시청/찜 */
const seen          = ref(false)
const liked         = ref(false)
const checked       = ref(false)
const likeChecked   = ref(false)

/* 유튜브 */
const reviewVideos       = ref([])   // 리뷰 – 3개씩 가로 스크롤
const shortsVideos       = ref([])   // 쇼츠 – 4개씩 가로 스크롤(세로 긴 비율)
const reviewPage        = ref(1)
const shortsPage        = ref(1)
const reviewsLoading    = ref(false)
const shortsLoading     = ref(false)
const youtubeErr        = ref('')

const activeVideoId = ref(null)  // 팝업으로 띄울 영상 ID
const closeVideo = () => activeVideoId.value = null

const ottFlatrate = computed(() => movie.value?.watch_providers?.flatrate || [])
const ottLink = computed(() => movie.value?.watch_providers?.link || null)

const relatedMovies = computed(() => movie.value?.related_movies || [])

const movieStore   = useMovieStore()

/* ───────────────────────── API helpers ───────────────────────── */
async function fetchMovie () {
  const id = Number(route.params.id)
  if (!id) {
    error.value   = '올바른 영화 ID가 아닙니다.'
    loading.value = false
    return
  }
  try {
    const { data } = await api.get(`api/recommend/tmdb/${id}/`)
    movie.value = data
  } catch (e) {
    console.error(e)
    error.value = '영화 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function pickThumb(thumbnails, videoId) {
  return (
    thumbnails?.maxres?.url ||
    thumbnails?.standard?.url ||
    thumbnails?.high?.url ||
    thumbnails?.medium?.url ||
    thumbnails?.default?.url ||
    `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`
  )
}

/* ─── 유튜브 검색 ───────────────────────────── */
async function searchYoutube (category, page) {
  const params = {
    title   : movie.value.title,
    category,
    page,
  }
  try {
    const { data } = await api.get('/api/recommend/youtube/search/', { params })
    return data.map(item => ({
   videoId: item.videoId,
      title: item.title,
   channel: item.channel,
   thumbnail: pickThumb(item.thumbnails, item.videoId)
 }))
  } catch (e) {
    console.error('YouTube 검색 실패', e)
    youtubeErr.value = '유튜브 영상을 불러오지 못했습니다.'
    return []
  }
}

async function loadReviews (initial=false) {
  if (reviewsLoading.value) return
  reviewsLoading.value = true
  if (initial) reviewPage.value = 1
  const list = await searchYoutube('리뷰', reviewPage.value)
  if (initial) reviewVideos.value = list
  else reviewVideos.value.push(...list)
  reviewPage.value += 1
  reviewsLoading.value = false
}

async function loadShorts  (initial=false) {
  if (shortsLoading.value) return
  shortsLoading.value = true
  if (initial) shortsPage.value = 1
  const list = await searchYoutube('명장면 쇼츠', shortsPage.value)
  if (initial) shortsVideos.value = list
  else shortsVideos.value.push(...list)
  shortsPage.value += 1
  shortsLoading.value = false
}

/* ─── 시청/찜 helpers (기존) ─────────────────── */
async function checkWatchHistory () {
  try {
    const { data } = await api.get(`/accounts/history/check/${route.params.id}/`)
    seen.value = data.seen
  } catch (e) { console.error(e) } finally { checked.value = true }
}
async function addToWatchHistory () {
  try { await api.post(`/accounts/history/add/`, { tmdb_id:Number(route.params.id) }) ; seen.value = true } catch(e){console.error(e)}
}
async function removeFromWatchHistory () {
  try { await api.delete(`/accounts/history/remove/${route.params.id}/`) ; seen.value=false } catch(e){console.error(e)}
}
async function checkFavorite () {
  try { const { data } = await api.get(`/accounts/favorites/check/${route.params.id}/`) ; liked.value = data.liked } catch(e){console.error(e)} finally { likeChecked.value=true }
}
async function toggleFavorite () {
  try {
    if (liked.value) { await api.delete(`/accounts/favorites/remove/${route.params.id}/`) ; liked.value=false }
    else { await api.post(`/accounts/favorites/add/`, { tmdb_id:Number(route.params.id) }) ; liked.value=true }
  } catch(e){console.error(e)}
}

/* ───────────────────── 마운트 & Watch ───────────────────── */
onMounted(fetchMovie)

watch(movie, (m) => {
  if (!m?.title) return
  checkWatchHistory(); checkFavorite()
  loadReviews(true);    // 초기 6개 – 3*2줄 대신 3개 가로 스크롤
  loadShorts(true)      // 초기 4개 가로 스크롤
})

/* ───────────────────────── 계산 속성 ───────────────────────── */
const matched = computed(()=> movieStore.results.find(m=>m.id===Number(route.params.id)))
const reason  = computed(()=> matched.value?.reason || '')

const director = computed(()=> movie.value?.credits?.crew?.find(c=>c.job==='Director'))
const castCards = computed(()=>{
  const arr=[]; if(director.value){arr.push({id:director.value.id,name:director.value.name,role:'감독',profile:director.value.profile_path})}
  movie.value?.credits?.cast?.slice(0,10).forEach(c=>arr.push({id:c.id,name:c.name,role:c.character||'출연',profile:c.profile_path}))
  return arr
})

/* ─────────────────── 가로 스크롤 유틸 ─────────────────── */
function scrollByPx(el, px){ el?.scrollBy({left:px,behavior:'smooth'}) }


// ▼ 추가 : 영상 ID → 썸네일 URL  
function ytThumb (id, isShorts = false) {
  /* 16:9 리뷰 : hqdefault (480×360)
     9:16 쇼츠 : hq720     (720×1280, 세로형) */
  const quality = isShorts ? 'hq720' : 'hqdefault'
  return `https://i.ytimg.com/vi/${id}/${quality}.jpg`
}
</script>

<template>
  <section class="container my-4">
    <!-- 로딩 & 에러 -->
    <div v-if="loading" class="text-center py-5">
      <span class="spinner-border" role="status" aria-hidden="true" />
      <p class="mt-3">불러오는 중…</p>
    </div>
    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <!-- 정상 화면 -->
    <div v-else class="row g-4">
      <!-- 포스터 -->
      <div class="col-md-4 text-center">
        <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500'+movie.poster_path" :alt="movie.title" class="img-fluid rounded shadow" />
        <div v-else class="bg-secondary text-white p-5 rounded">포스터 없음</div>
      </div>

      <!-- 정보 -->
      <div class="col-md-8">
        <h2 class="fw-bold">{{ movie.title }}</h2>
        <p class="text-muted mb-1">평점 ★ {{ movie.vote_average?.toFixed(1) ?? 'N/A' }}</p>
        <p>{{ movie.overview || '줄거리 정보가 없습니다.' }}</p>

        <!-- 찜 & 시청 토글 -->
        <div class="d-flex gap-3 flex-wrap align-items-center mt-3">
          <!-- 찜 버튼 -->
          <button
            v-if="likeChecked"
            class="btn btn-sm animated-toggle"
            :class="liked ? 'btn-danger' : 'btn-outline-danger'"
            @click="toggleFavorite"
            style="min-width: 150px"
          >
            ❤️ {{ liked ? '찜한 영화입니다' : '찜하기' }}
          </button>

          <!-- 시청 버튼 -->
          <button
            v-if="checked"
            class="btn btn-sm animated-toggle"
            :class="seen ? 'btn-outline-secondary' : 'btn-outline-primary'"
            @click="seen ? removeFromWatchHistory() : addToWatchHistory()"
            style="min-width: 150px"
          >
            👁️ {{ seen ? '이미 본 영화입니다' : '봤어요' }}
          </button>
        </div>

        <p v-if="reason" class="text-muted fst-italic mt-3">🧠 이 영화를 추천한 이유: {{ reason }}</p>

        <!-- OTT 감상처 안내 -->
        <div v-if="ottFlatrate.length" class="mt-3">
          <h5 class="mb-2">📺 감상 가능한 OTT</h5>
          <a
            v-for="provider in ottFlatrate"
            :key="provider.provider_id"
            :href="ottLink"
            target="_blank"
            rel="noopener"
            class="ott-badge me-2 d-inline-flex align-items-center justify-content-center"
            :title="provider.provider_name"
          >
            <img
              :src="'https://image.tmdb.org/t/p/w92' + provider.logo_path"
              :alt="provider.provider_name"
              class="ott-logo"
            />
          </a>
        </div>


        <!-- 장르 & 개봉일 -->
        <div v-if="movie.genres?.length" class="mt-4">
          <h5 class="mb-2">장르</h5>
          <span v-for="g in movie.genres" :key="g.id" class="badge bg-primary me-2">{{ g.name }}</span>
        </div>
        <div v-if="movie.release_date" class="mt-3"><small class="text-muted">개봉일: {{ movie.release_date }}</small></div>
      </div>

      <!-- 감독/출연 캐러셀 -->
      <div v-if="castCards.length" class="col-12 mt-2 position-relative">
        <h4 class="mb-3">감독 / 출연</h4>
        <button class="carousel-btn start-0" @click="scrollByPx($refs.castRow,-300)">‹</button>
        <button class="carousel-btn end-0"   @click="scrollByPx($refs.castRow, 300)">›</button>
        <div ref="castRow" class="cast-scroll d-flex gap-3 overflow-auto pb-2">
          <div v-for="p in castCards" :key="p.id" class="text-center flex-shrink-0" style="width:110px;">
            <transition name="fade" appear>
              <img v-if="p.profile" :src="'https://image.tmdb.org/t/p/w185'+p.profile" class="rounded-circle cast-photo mb-2" :alt="p.name" loading="lazy" />
              <div v-else class="rounded-circle bg-secondary d-flex align-items-center justify-content-center text-white mb-2" style="width:100px;height:100px"><i class="bi bi-person fs-2"/></div>
            </transition>
            <div class="small fw-semibold text-truncate">{{ p.name }}</div>
            <div class="small text-muted text-truncate">{{ p.role }}</div>
          </div>
        </div>
      </div>

      <MovieArticleList />

      <!-- 리뷰 영상 -->
      <div v-if="reviewVideos.length" class="col-12 mt-5">
        <h4 class="mb-3">🎬 유튜브 리뷰 영상</h4>
        <div class="scroll-row" ref="reviewRow">
          <div v-for="v in reviewVideos" :key="v.videoId" class="video-card flex-shrink-0">
            <div @click="activeVideoId = v.videoId" class="text-decoration-none" style="cursor: pointer;">
              <img :src="ytThumb(v.videoId)" :alt="v.title" class="thumb w-100" />
              <div class="p-2">
                <div class="fw-semibold text-dark small text-truncate">{{ v.title }}</div>
                <div class="text-muted small text-truncate">{{ v.channel }}</div>
              </div>
            </div>
          </div>
          <button class="more-card" @click="loadReviews()" v-if="!reviewsLoading">
            더보기 »
          </button>
          <div class="more-card" v-else><span class="spinner-border spinner-border-sm"/></div>
        </div>
      </div>

      <!-- 쇼츠 영상 -->
      <div v-if="shortsVideos.length" class="col-12 mt-5">
        <h4 class="mb-3">📱 유튜브 쇼츠</h4>
        <div class="scroll-row" ref="shortsRow">
          <div v-for="s in shortsVideos" :key="s.videoId" class="shorts-card flex-shrink-0">
            <div @click="activeVideoId = s.videoId" style="cursor: pointer;">
              <img :src="s.thumbnail" :alt="s.title" class="thumb w-100" />
            </div>
          </div>
          <button class="more-card" @click="loadShorts()" v-if="!shortsLoading">더보기 »</button>
          <div class="more-card" v-else><span class="spinner-border spinner-border-sm"/></div>
        </div>
      </div>

      <!-- 연관 영화 추천 -->
      <div v-if="relatedMovies.length" class="col-12 mt-5">
        <h4 class="mb-3">🎬 이 영화를 본 사람들이 좋아한 작품</h4>
        <div class="scroll-row">
          <router-link
            v-for="r in relatedMovies"
            :key="r.id"
            :to="`/detail/${r.id}`"
            class="text-decoration-none text-dark flex-shrink-0"
            style="width: 200px"
          >
            <div class="card h-100 shadow-sm">
              <img
                v-if="r.poster_path"
                :src="'https://image.tmdb.org/t/p/w500' + r.poster_path"
                class="card-img-top"
                :alt="r.title"
              />
              <div class="card-body">
                <h6 class="card-title text-truncate">{{ r.title }}</h6>
                <p class="card-text text-muted small">★ {{ r.vote_average.toFixed(1) }}</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
    <!-- 유튜브 팝업 플레이어 -->
      <div v-if="activeVideoId" class="yt-overlay" @click.self="closeVideo">
        <div class="yt-player">
          <button class="btn-close float-end" @click="closeVideo" />
          <iframe
            :src="`https://www.youtube.com/embed/${activeVideoId}?autoplay=1&rel=0`"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
            width="100%"
            height="100%"
          ></iframe>
        </div>
      </div>
  </section>
</template>

<style scoped>
img { max-height: 540px; object-fit: cover; }
.cast-photo{width:100px;height:100px;object-fit:cover}
.fade-enter-from,.fade-leave-to{opacity:0;transform:scale(.95)}
.fade-enter-active,.fade-leave-active{transition:opacity .4s ease,transform .4s ease}
.cast-scroll::-webkit-scrollbar{height:6px}
.cast-scroll::-webkit-scrollbar-thumb{background:#ced4da;border-radius:3px}
.carousel-btn{position:absolute;top:50%;translate:0 -50%;border:none;background:rgba(255,255,255,.85);width:32px;height:32px;border-radius:50%;font-size:20px;line-height:20px;padding:0;color:#495057;box-shadow:0 0 4px rgba(0,0,0,.15);z-index:1}
.carousel-btn:hover{background:#f1f3f5}
.carousel-btn:focus{outline:none;box-shadow:0 0 0 3px rgba(0,123,255,.25)}

/* ─── 리뷰/쇼츠 스크롤 행 ─── */
.scroll-row{display:flex;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:.5rem}
.scroll-row::-webkit-scrollbar{height:8px}
.scroll-row::-webkit-scrollbar-thumb{background:#ced4da;border-radius:4px}

.video-card{width:320px;scroll-snap-align:start;border:1px solid #dee2e6;border-radius:.5rem;overflow:hidden;background:#fff}
.shorts-card{width:200px;scroll-snap-align:start;border:1px solid #dee2e6;border-radius:.5rem;overflow:hidden;background:#fff}
.shorts-card .thumb{aspect-ratio:9/16;object-fit:cover}
.video-card .thumb{aspect-ratio:16/9;object-fit:cover}

.more-card{display:flex;align-items:center;justify-content:center;width:100px;min-width:100px;scroll-snap-align:start;border:2px dashed #868e96;background:#f8f9fa;border-radius:.5rem;font-weight:600;color:#495057}
.more-card:hover{background:#e9ecef;cursor:pointer}

.yt-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.7);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.yt-player {
  width: 90%;
  max-width: 720px;
  aspect-ratio: 16 / 9;
  background: #000;
  position: relative;
  border-radius: .5rem;
  overflow: hidden;
}
.btn-close {
  position: absolute;
  top: .5rem;
  right: .5rem;
  z-index: 1;
}

.ott-badge {
  width: 56px;
  height: 56px;
  border-radius: 0.5rem;
  background-color: #f1f3f5;
  transition: all 0.2s ease;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}
.ott-badge:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}
.ott-logo {
  width: 70%;
  height: 70%;
  object-fit: contain;
}
.animated-toggle {
  transition: transform 0.2s ease;
  transform: scale(1);
}
.animated-toggle:active {
  transform: scale(1.08);
}


</style>
