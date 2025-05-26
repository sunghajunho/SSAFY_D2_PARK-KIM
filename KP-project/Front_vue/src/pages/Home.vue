<script setup>
import { ref, watch } from 'vue'
import { useThemeStore } from '@/stores/themeStore'
import RecommendedPreview from '@/components/RecommendedPreview.vue'
import { useUserStore } from '@/stores/userStore'

const query = ref('')
const themeStore = useThemeStore()

const mood = ref('')
const situation = ref('')
const genres = ref([])

// ✅ ‘기분’ – 메이저 OTT에서 자주 쓰이는 감성 키워드 10선
const moodOptions = ['힐링되는', '감동적인', '유쾌한', '스릴 넘치는', '긴장감 있는',
                     '따뜻한', '로맨틱한', '웃긴', '우울한', '무서운']

// ✅ ‘상황’ – 시청 시나리오별 10선
const situationOptions = ['혼자 볼 때', '연인과 함께', '가족과 함께', '친구들과 파티용',
                          '휴가 중', '출퇴근길', '집중해서 볼 때', '배경으로 틀어놓기',
                          '비 오는 날', '주말 밤']

// ✅ ‘장르’ – TMDB 인기·수록량 상위 순으로 정렬
const genreOptions = ['드라마', '액션', '코미디', '스릴러', '로맨스', 'SF', '모험',
                      '애니메이션', '공포', '범죄', '판타지', '다큐멘터리', '가족',
                      '미스터리', '역사', '음악', '서부', '전쟁', 'TV 영화']


const userStore = useUserStore()
const model = ref(userStore.model)

function buildPrompt() {
  let prompt = ''

  if (mood.value) prompt += `${mood.value} 분위기의 `
  if (situation.value) prompt += `${situation.value} `
  if (genres.value.length > 0) prompt += `${genres.value.join(', ')} 장르의 `
  if (prompt) prompt += '영화 중, '

  if (query.value.trim()) {
    prompt += `'${query.value}'와 어울리는 영화를 추천해줘.`
  } else {
    prompt += '추천할 만한 영화를 알려줘.'
  }

  return prompt
}

function searchCombined() {
  const prompt = buildPrompt()
  if (!prompt.trim()) return
  const base = `/results?q=${encodeURIComponent(prompt)}`
  const full = `${base}&model=${encodeURIComponent(model.value)}`
  window.location.href = full
}

watch(model, (val) => {
  userStore.setModel(val)
})
</script>

<template>
  <div class="container text-center mt-5">
    <h1 class="display-4 mb-4 fw-bold">🎬 MovieGPT</h1>
    <p class="lead text-muted mb-4">GPT와 함께, 당신의 취향을 읽는 영화 추천</p>

    <!-- 검색어 + 조건 필터 통합 영역 -->
    <div class="mb-4">
      <div class="input-group input-group-lg mx-auto" style="max-width: 600px;">
        <input v-model="query" class="form-control" placeholder="영화를 찾아보세요..." />
        <button class="btn btn-primary" @click="searchCombined">🎯 추천 받기</button>
      </div>

      <!-- 조건 필터 UI -->
      <div class="text-start mt-4" style="max-width: 600px; margin: auto;">
        <!-- 기분 선택 -->
        <div class="mb-2">
          <label class="me-2 fw-bold">기분:</label>
          <button
            v-for="option in moodOptions"
            :key="option"
            class="btn btn-sm me-1 mb-1"
            :class="mood === option ? 'btn-primary' : 'btn-outline-primary'"
            @click="mood = option"
          >
            {{ option }}
          </button>
        </div>

        <!-- 상황 선택 -->
        <div class="mb-2">
          <label class="me-2 fw-bold">상황:</label>
          <button
            v-for="option in situationOptions"
            :key="option"
            class="btn btn-sm me-1 mb-1"
            :class="situation === option ? 'btn-secondary' : 'btn-outline-secondary'"
            @click="situation = option"
          >
            {{ option }}
          </button>
        </div>

        <!-- 장르 선택 -->
        <div class="mb-3">
          <label class="fw-bold me-2">장르:</label>
          <div class="d-inline-block" v-for="option in genreOptions" :key="option">
            <input
              type="checkbox"
              class="form-check-input me-1"
              :id="option"
              :value="option"
              v-model="genres"
            />
            <label class="form-check-label me-3" :for="option">{{ option }}</label>
          </div>
        </div>
        <div class="mb-3">
          <label for="modelSelect" class="fw-bold me-2">모델 선택:</label>
          <select id="modelSelect" v-model="model" class="form-select d-inline-block w-auto">
            <option value="gpt-4">🧠 GPT-4 (정확도 우선)</option>
            <option value="gpt-3.5-turbo">⚡ GPT-3.5 (속도 우선)</option>
          </select>
        </div>
      </div>
    </div>

    <hr class="my-4" />

    <RecommendedPreview />

    <div class="mt-5">
      <button class="btn btn-outline-secondary btn-sm" @click="themeStore.toggleTheme">
        🌗 테마 전환 ({{ themeStore.theme === 'light' ? '라이트' : '다크' }})
      </button>
    </div>
  </div>
</template>
