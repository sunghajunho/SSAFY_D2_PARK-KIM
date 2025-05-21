import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: 'light',
  }),
  actions: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light'
      document.documentElement.setAttribute('data-bs-theme', this.theme)
    },
    initTheme() {
      document.documentElement.setAttribute('data-bs-theme', this.theme)
    },
  },
})
