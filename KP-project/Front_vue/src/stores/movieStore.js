import { defineStore } from 'pinia'

export const useMovieStore = defineStore('movie', {
  state: () => ({
    query: '',
    results: [],
    recommended: [], // ✅ 추가
    recommendedAt: null,
  }),
  actions: {
    setQuery(q) {
      this.query = q
    },
    setResults(list) {
      this.results = list
    },
    setRecommended(list) {  // ✅ 추가
      this.recommended = list
      this.recommendedAt = Date.now()
    },
  },
})