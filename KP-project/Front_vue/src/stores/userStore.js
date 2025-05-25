// src/stores/userStore.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api/axios'  // ✅ 공통 인스턴스를 사용

export const useUserStore = defineStore('user', () => {
  const ACCOUNT_API_URL = 'accounts'  // baseURL에서 이미 / 붙었음

  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const nickname = ref(localStorage.getItem('nickname') || '')

  const isLoggedIn = computed(() => !!token.value)

  // ✅ 회원가입
  const register = async (form) => {
    try {
      const res = await api.post(`${ACCOUNT_API_URL}/signup/`, form)
      token.value = res.data.key
      localStorage.setItem('token', token.value)
      await fetchUserInfo()
    } catch (err) {
      console.error('회원가입 실패:', err.response?.data || err)
      throw err
    }
  }

  // ✅ 로그인
  const logIn = async ({ username, password }) => {
    try {
      const res = await api.post(`${ACCOUNT_API_URL}/login/`, {
        username,
        password,
      })
      token.value = res.data.key
      localStorage.setItem('token', token.value)
      await fetchUserInfo()
      return true
    } catch (err) {
      console.error('로그인 실패:', err.response?.data || err)
      return false
    }
  }

  // ✅ 사용자 정보 불러오기
  const fetchUserInfo = async () => {
    try {
      const res = await api.get(`${ACCOUNT_API_URL}/user/`)
      username.value = res.data.username
      nickname.value = res.data.nickname
      localStorage.setItem('username', username.value)
      localStorage.setItem('nickname', nickname.value)
    } catch (err) {
      console.error('사용자 정보 로드 실패:', err)
    }
  }

  // ✅ 로그아웃
  const logout = () => {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  // ✅ 특정 사용자 프로필 가져오기
  const getUserProfile = async (usernameParam) => {
    try {
      const res = await api.get(`/accounts/profile/${usernameParam}/`)
      return res.data
    } catch (err) {
      console.error('사용자 프로필 로드 실패:', err)
      return null
    }
  }


  return {
    token,
    username,
    nickname,
    isLoggedIn,
    register,
    logIn,
    fetchUserInfo,
    logout,
    getUserProfile,
  }
}, {
  persist: true,
})



