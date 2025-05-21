import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const instance = axios.create({
  baseURL: 'http://localhost:8000/', // 또는 실제 배포 주소
  timeout: 10000,
})

// 요청 시 Authorization 토큰 추가
instance.interceptors.request.use((config) => {
  const userStore = useUserStore()
  const token = userStore.token
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default instance
