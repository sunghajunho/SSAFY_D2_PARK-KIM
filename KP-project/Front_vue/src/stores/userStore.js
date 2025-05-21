// src/stores/userStore.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  const isLoggedIn = computed(() => !!token.value)

  const register = async (userInfo) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/signup/`, userInfo)
      token.value = res.data.key
      localStorage.setItem('token', token.value)
      await fetchUserInfo()
    } catch (err) {
      console.error('회원가입 실패:', err.response?.data || err)
    }
  }

  const login = async ({ email, password }) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/login/`, { email, password })
      token.value = res.data.key
      localStorage.setItem('token', token.value)
      await fetchUserInfo()
    } catch (err) {
      console.error('로그인 실패:', err.response?.data || err)
    }
  }

  const fetchUserInfo = async () => {
    try {
      const res = await axios.get(`${ACCOUNT_API_URL}/user/`, {
        headers: { Authorization: `Token ${token.value}` }
      })
      username.value = res.data.username
      localStorage.setItem('username', username.value)
    } catch (e) {
      console.error('사용자 정보 불러오기 실패:', e)
    }
  }

  const logout = () => {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, isLoggedIn, register, login, logout }
})

