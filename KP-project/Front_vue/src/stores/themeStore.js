import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({ theme: localStorage.getItem('theme') ?? 'light' }),
  actions: {
    toggleTheme() {
  this.theme = this.theme === 'light' ? 'dark' : 'light'
  localStorage.setItem('theme', this.theme)
  document.documentElement.dataset.bsTheme = this.theme
    },
    initTheme() {
      document.documentElement.setAttribute('data-bs-theme', this.theme)
    },
  },
})
