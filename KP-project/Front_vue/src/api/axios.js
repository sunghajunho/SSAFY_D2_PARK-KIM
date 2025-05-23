// src/api/axios.js
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'
import { getActivePinia, setActivePinia, createPinia } from 'pinia'

/* ------------------------------------------------------------------
   1. 공통 인스턴스
      - baseURL은 .env(VITE_API_BASE_URL) → 없으면 localhost 로 폴백
   ----------------------------------------------------------------- */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/',
  headers: {
    'Content-Type': 'application/json',
  },
})

/* ------------------------------------------------------------------
   2. 요청 인터셉터
      - URL 앞 ‘/’ 제거: axios가 baseURL 뒤에 슬래시를 자동 붙이므로
      - Pinia가 아직 활성화되지 않은 경우를 대비해 임시로 활성화
      - 로그인 토큰이 있으면 Authorization 헤더 주입
   ----------------------------------------------------------------- */
api.interceptors.request.use((config) => {
  // (1) 슬래시 중복 방지
  if (config.url?.startsWith('/')) {
    config.url = config.url.slice(1)
  }

  // (2) Pinia 보증
  if (!getActivePinia()) {
    setActivePinia(createPinia())
  }
  const userStore = useUserStore()
  const token = userStore.token

  // (3) 토큰 주입
  if (token) {
    config.headers = {
      ...config.headers,                // 기존 헤더 유지
      Authorization: `Token ${token}`,
    }
  }

  return config
})

export default api
