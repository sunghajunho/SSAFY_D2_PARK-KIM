import { defineStore } from 'pinia'

export const useMovieStore = defineStore('movie', {
  state: () => ({
    query: '',
    results: [],
  }),
  actions: {
    setQuery(q) {
      this.query = q
    },
    setResults(list) {
      this.results = list
    },
  },
})
