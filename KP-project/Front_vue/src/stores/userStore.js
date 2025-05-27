// src/stores/userStore.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api/axios'  // ✅ 공통 인스턴스를 사용
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const ACCOUNT_API_URL = 'accounts'  // baseURL에서 이미 / 붙었음

  const model = ref(localStorage.getItem('model') || 'gpt-3.5-turbo')  // 초기화

  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const nickname = ref(localStorage.getItem('nickname') || '')
  const id = ref(localStorage.getItem('id') || '')
  const isLoggedIn = computed(() => !!token.value)
  const favoriteMovieIds = ref([])
  const favoriteGenres = ref([])

  const setModel = (val) => {
  model.value = val
  localStorage.setItem('model', val)
  }

  const deleteUserAccount = async () => {
    try {
      await api.delete('/accounts/delete/')
      // 로컬스토리지/토큰 정리 등 필요시
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('nickname')
      alert('회원탈퇴가 완료되었습니다.')
      window.location.href = '/'  // 홈으로 이동
    } catch (e) {
      console.error('회원탈퇴 실패:', e)
      alert('회원탈퇴에 실패했습니다.')
    }
  }

  const changePassword = async (currentPassword, newPassword) => {
    try {
      await api.post('/accounts/password/change/', {
        old_password: currentPassword,
        new_password1: newPassword,
        new_password2: newPassword
      })
      alert('비밀번호가 성공적으로 변경되었습니다.')
    } catch (e) {
      console.error('비밀번호 변경 실패:', e)
      alert('비밀번호 변경에 실패했습니다.')
    }
  }

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

      const { useMovieStore } = await import('@/stores/movieStore')
      const movieStore = useMovieStore()
      movieStore.clearRecommended()

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
      favoriteGenres.value = (res.data.preferred_genres || []).map(g => g.name)
      id.value = res.data.id
      localStorage.setItem('username', username.value)
      localStorage.setItem('nickname', nickname.value)
      localStorage.setItem('id', id.value)
    } catch (err) {
      console.error('사용자 정보 로드 실패:', err)
    }
  }

  // ✅ 프로필 정보 수정
  const updateProfile = async (formData) => {
    try {
      const res = await api.put('/accounts/profile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${token.value}`,
        },
      });
      // 업데이트 후, 최신 정보 다시 로드
      await fetchUserInfo();
      return res.data;
    } catch (err) {
      console.error('프로필 업데이트 실패:', err.response?.data || err);
      throw err;
    }
  };


  // ✅ 로그아웃
  const logout = async () => {
    token.value = ''
    username.value = ''
    favoriteGenres.value = []
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    const { useMovieStore } = await import('@/stores/movieStore')
    const movieStore = useMovieStore()
    movieStore.clearRecommended()
  }


  // ✅ 특정 사용자 프로필 가져오기
  const getUserProfile = async (usernameParam) => {
    try {
      const res = await api.get(`/accounts/profile/${usernameParam}/`)
      console.log(res.data)
      return res.data
    } catch (err) {
      console.error('사용자 프로필 로드 실패:', err)
      return null
    }
  }

  // ✅ 팔로우/언팔로우 토글
  const toggleFollow = async (followingId) => {
    try {
      const res = await api.post('/accounts/follows/toggle/', { following: followingId });
      return res.data.status;
    } catch (err) {
      console.error('팔로우 토글 실패:', err.response?.data || err);
      throw err;
    }
  };

  // ✅ 팔로워/팔로잉 상태 확인
  const getFollowStatus = async (username) => {
    try {
      const res = await api.get(`/accounts/follows/status/${username}/`);
      return res.data.is_following;
    } catch (err) {
      console.error('팔로우 상태 확인 실패:', err.response?.data || err);
      throw err;
    }
  };

  // ✅ 팔로워 리스트
  const getFollowers = async (username) => {
    try {
      const res = await api.get(`/accounts/follows/followers/${username}/`);
      return res.data.followers;
    } catch (err) {
      console.error('팔로워 조회 실패:', err.response?.data || err);
      throw err;
    }
  };

  // ✅ 팔로잉 리스트
  const getFollowing = async (username) => {
    try {
      const res = await api.get(`/accounts/follows/following/${username}/`);
      return res.data.following;
    } catch (err) {
      console.error('팔로잉 조회 실패:', err.response?.data || err);
      throw err;
    }
  };


  const fetchFavoriteMovies = async (username) => {
      try {
        const url = username
        ? `/accounts/favorite-movies/${username}/`
        : `/accounts/favorite-movies/`
        const res = await api.get(url)
        favoriteMovieIds.value = res.data.tmdb_ids
      } catch (e) {
        console.error('찜한 영화 목록 가져오기 실패', e)
      }
    };


  return {
    token,
    username,
    nickname,
    isLoggedIn,
    favoriteMovieIds,
    model,
    favoriteGenres,
    setModel,
    register,
    deleteUserAccount,
    changePassword,
    logIn,
    fetchUserInfo,
    logout,
    getUserProfile,
    updateProfile,
    toggleFollow,
    getFollowStatus,
    getFollowers,
    getFollowing,
    fetchFavoriteMovies,
  }
}, {
  persist: true,
})





