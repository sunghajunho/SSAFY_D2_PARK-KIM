// src/api/axios.js
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const api = axios.create({
  baseURL: 'http://localhost:8000/', // Django API 주소
  headers: {
    'Content-Type': 'application/json',
  },
})

// 토큰 자동 주입
api.interceptors.request.use((config) => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Token ${userStore.token}`
    console.log(config.headers.Authorization)
  }
  return config
})

export default api
