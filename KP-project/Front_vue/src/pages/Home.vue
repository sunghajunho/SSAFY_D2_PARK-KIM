<script setup>
import { ref, watch, computed } from 'vue'
import RecommendedPreview from '@/components/RecommendedPreview.vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'

const query = ref('')

const mood = ref('')
const situation = ref('')
const genres = ref([])

const showMood = ref(false)
const showSituation = ref(false)
const showGenres = ref(false)

const router = useRouter()
const movieStore = useMovieStore()

const moodOptions = ['힐링되는', '감동적인', '유쾌한', '스릴 넘치는', '긴장감 있는',
                     '따뜻한', '로맨틱한', '웃긴', '우울한', '무서운']

const situationOptions = ['혼자 볼 때', '연인과 함께', '가족과 함께', '친구들과 파티용',
                          '휴가 중', '출퇴근길', '집중해서 볼 때', '배경으로 틀어놓기',
                          '비 오는 날', '주말 밤']

const genreOptions = ['드라마', '액션', '코미디', '스릴러', '로맨스', 'SF', '모험',
                      '애니메이션', '공포', '범죄', '판타지', '다큐멘터리', '가족',
                      '미스터리', '역사', '음악', '서부', '전쟁', 'TV 영화']

const userStore = useUserStore()
const model = computed({
  get: () => userStore.model,
  set: (val) => userStore.setModel(val)
})

function buildPrompt() {
  const parts = []
  if (mood.value) parts.push(`${mood.value} 분위기`)
  if (situation.value) parts.push(`${situation.value}`)
  if (genres.value.length > 0) parts.push(`${genres.value.join(', ')} 장르`)

  const conditionText = parts.length > 0
    ? parts.join('에서 ') + ' 볼만한'
    : ''

  if (query.value.trim()) {
    return `${conditionText} 영화 중 '${query.value}'와 어울리는 작품을 추천해줘.`
  } else {
    return `${conditionText} 영화를 추천해줘.`
  }
}

function searchCombined() {
  const prompt = buildPrompt()
  if (!prompt.trim()) return

  // ✅ 조건 저장
  movieStore.setConditions({
    mood: mood.value,
    situation: situation.value,
    genres: [...genres.value],
  })

  // ✅ 이동
  router.push({
    name: 'Results',
    query: {
      q: prompt,
      model: model.value,
    }
  })
}

watch(model, (val) => {
  userStore.setModel(val)
})
</script>

<template>
  <div class="container text-center mt-5">
    <h1 class="display-4 mb-4 fw-bold">MovieGPT</h1>
    <p class="lead text-muted mb-4">GPT와 함께, 당신의 취향을 읽는 영화 추천</p>

    <div class="mb-4">
      <form
        @submit.prevent="searchCombined"
        class="input-group input-group-lg mx-auto"
        style="max-width: 600px;"
      >
        <input
          v-model="query"
          class="form-control"
          placeholder="영화를 찾아보세요..."
        />
        <button
          type="submit"
          class="btn btn-primary"
        >
          🎯 추천 받기
        </button>
      </form>

      <div class="row text-start mt-5 g-4">
        <!-- 기분 선택 -->
          <div class="col-md-4 border-end pe-4">
            <h5 class="fw-bold mb-2 d-flex justify-content-between align-items-center">
              <span>🎭 기분</span>
              <button class="btn btn-sm btn-outline-secondary" @click="showMood ? (mood = '', showMood = false) : showMood = true">
                {{ showMood ? '선택 안함' : '열기' }}
              </button>
            </h5>
          <div v-if="showMood" class="border rounded p-3" style="max-height: 200px; overflow-y: auto;">
            <div v-for="option in moodOptions" :key="option" class="form-check mb-2">
              <input
                type="radio"
                class="form-check-input"
                :id="'mood-' + option"
                :value="option"
                v-model="mood"
              />
              <label class="form-check-label" :for="'mood-' + option">{{ option }}</label>
            </div>
          </div>
        </div>

        <!-- 상황 선택 -->
        <div class="col-md-4 border-end pe-4">
          <h5 class="fw-bold mb-2 d-flex justify-content-between align-items-center">
            <span>🕰️ 상황</span>
            <button class="btn btn-sm btn-outline-secondary" @click="showSituation ? (situation = '', showSituation = false) : showSituation = true">
              {{ showSituation ? '선택 안함' : '열기' }}
            </button>
          </h5>
          <div v-if="showSituation" class="border rounded p-3" style="max-height: 200px; overflow-y: auto;">
            <div v-for="option in situationOptions" :key="option" class="form-check mb-2">
              <input
                type="radio"
                class="form-check-input"
                :id="'situation-' + option"
                :value="option"
                v-model="situation"
              />
              <label class="form-check-label" :for="'situation-' + option">{{ option }}</label>
            </div>
          </div>
        </div>

        <!-- 장르 선택 -->
        <div class="col-md-4 border-end pe-4">
          <h5 class="fw-bold mb-2 d-flex justify-content-between align-items-center">
            <span>🎬 장르</span>
            <button class="btn btn-sm btn-outline-secondary" @click="showGenres ? (genres = [], showGenres = false) : showGenres = true">
              {{ showGenres ? '선택 안함' : '열기' }}
            </button>
          </h5>
          <div v-if="showGenres" class="border rounded p-3" style="max-height: 200px; overflow-y: auto;">
            <div v-for="option in genreOptions" :key="option" class="form-check mb-2">
              <input
                type="checkbox"
                class="form-check-input"
                :id="'genre-' + option"
                :value="option"
                v-model="genres"
              />
              <label class="form-check-label" :for="'genre-' + option">{{ option }}</label>
            </div>
          </div>
          <small class="text-muted">복수 선택 가능</small>
        </div>
      </div>
    </div>
    <div class="my-4">
      <label class="fw-bold me-3">누가 추천할까요?</label><br><br>
      <div class="btn-group" role="group">
        <input
          type="radio"
          class="btn-check"
          name="model"
          id="gpt4"
          value="gpt-4"
          v-model="model"
          autocomplete="off"
        />
        <label class="btn btn-outline-primary" for="gpt4">정확 🧠 GPT-4</label>

        <input
          type="radio"
          class="btn-check"
          name="model"
          id="gpt35"
          value="gpt-3.5-turbo"
          v-model="model"
          autocomplete="off"
        />
        <label class="btn btn-outline-primary" for="gpt35">GPT-3.5 ⚡ 속도</label>
      </div>
    </div>


    <hr class="my-4" />
    <RecommendedPreview />

  </div>
</template>
