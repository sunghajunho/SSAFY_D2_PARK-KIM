// src/stores/userStore.js
import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login({ email, password }) {
      const res = await api.post('/accounts/login/', { email, password })
      this.token = res.data.key
      localStorage.setItem('token', this.token)
      await this.fetchUserInfo()
    },

    async register({ email, username, password1, password2 }) {
      const res = await api.post('/accounts/signup/', {
        email, username, password1, password2
      })
      this.token = res.data.key
      localStorage.setItem('token', this.token)
      await this.fetchUserInfo()
    },

    async fetchUserInfo() {
      try {
        const res = await api.get('/user/')
        this.username = res.data.username
        localStorage.setItem('username', this.username)
      } catch (e) {
        console.error('사용자 정보 불러오기 실패:', e)
      }
    },

    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    },
  },
})
