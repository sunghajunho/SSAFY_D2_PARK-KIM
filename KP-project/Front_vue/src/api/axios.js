// src/api/axios.js
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'
import { getActivePinia, setActivePinia, createPinia } from 'pinia'
import router from '@/router' // ✅ 라우터 접근 추가

/* ------------------------------------------------------------------
   1. 공통 인스턴스
      - baseURL은 .env(VITE_API_BASE_URL) → 없으면 localhost 로 폴백
   ----------------------------------------------------------------- */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/',
  withCredentials: true,
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
      ...config.headers,
      Authorization: `Token ${token}`,
    }
  }

  return config
})

/* ------------------------------------------------------------------
   3. 응답 인터셉터 (401 처리)
      - 인증 실패 시 로그아웃 + 로그인 페이지 이동
   ----------------------------------------------------------------- */
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      alert('세션이 만료되었습니다. 다시 로그인해 주세요.')
      if (!getActivePinia()) {
        setActivePinia(createPinia())
      }
      const userStore = useUserStore()
      userStore.logout()
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default api
