import { defineStore } from 'pinia'

export const useMovieStore = defineStore('movie', {
  state: () => ({
    query: '',
    results: [],
    recommended: [],
    recommendedAt: null,

    // ✅ 새로 추가: 사용자가 선택한 조건들
    conditions: {
      mood: '',
      situation: '',
      genres: [],
    },
  }),
  actions: {
    setQuery(q) {
      this.query = q
    },
    setResults(list) {
      this.results = list
    },
    setRecommended(list) {
      this.recommended = list
      this.recommendedAt = Date.now()
    },
    clearRecommended() {
      this.recommended = []
      this.recommendedAt = null
    },
    // ✅ 새로 추가: 조건 저장 액션
    setConditions({ mood, situation, genres }) {
      this.conditions.mood = mood
      this.conditions.situation = situation
      this.conditions.genres = genres
    },
  },
})
