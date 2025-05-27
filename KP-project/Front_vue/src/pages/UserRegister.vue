<template>
  <div class="register-container">
    <form class="register-form" @submit.prevent="onRegister">
      <h2 class="form-title">회원가입</h2>

      <div class="form-group"><input type="text" placeholder="Username" v-model="form.username" /></div>
      <div class="form-group"><input type="email" placeholder="Email" v-model="form.email" /></div>
      <div class="form-group"><input type="password" placeholder="Password" v-model="form.password1" /></div>
      <div class="form-group"><input type="password" placeholder="Password 확인" v-model="form.password2" /></div>
      <div class="form-group"><input type="text" placeholder="Real Name" v-model="form.real_name" /></div>
      <div class="form-group"><input type="text" placeholder="Nickname" v-model="form.nickname" /></div>
      <div class="form-group"><input type="number" placeholder="Age" v-model.number="form.age" /></div>

      <div class="form-group">
        <select v-model="form.gender">
          <option disabled value="">성별 선택</option>
          <option>남성</option>
          <option>여성</option>
        </select>
      </div>

      <div class="form-group">
        <select v-model="form.mbti">
          <option disabled value="">MBTI 선택</option>
          <option v-for="mbti in mbtis" :key="mbti">{{ mbti }}</option>
        </select>
      </div>

      <div class="form-group">
        <select v-model="form.region">
          <option disabled value="">지역 선택</option>
          <option v-for="region in regions" :key="region">{{ region }}</option>
        </select>
      </div>

      <!-- ✅ 선호 장르 우선순위 (중복 방지) -->
      <div class="form-group genre-priority">
        <label>1순위 장르:</label>
        <select v-model="firstGenre">
          <option disabled value="">선택</option>
          <option v-for="genre in genres" :key="genre.id" :value="genre.id">{{ genre.name }}</option>
        </select>
      </div>

      <div class="form-group genre-priority">
        <label>2순위 장르:</label>
        <select v-model="secondGenre">
          <option disabled value="">선택</option>
          <option v-for="genre in filteredGenresForSecond" :key="genre.id" :value="genre.id">{{ genre.name }}</option>
        </select>
      </div>

      <div class="form-group genre-priority">
        <label>3순위 장르:</label>
        <select v-model="thirdGenre">
          <option disabled value="">선택</option>
          <option v-for="genre in filteredGenresForThird" :key="genre.id" :value="genre.id">{{ genre.name }}</option>
        </select>
      </div>

      <button class="submit-btn" type="submit">회원가입</button>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

// ✅ 회원가입 폼
const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  real_name: '',
  nickname: '',
  age: null,
  gender: '',
  mbti: '',
  region: '',
  preferred_genres: [] // 최종 전송할 preferred_genres 배열
})

// ✅ 1순위, 2순위, 3순위 드롭다운
const firstGenre = ref('')
const secondGenre = ref('')
const thirdGenre = ref('')

const genres = ref([])
const mbtis = ['INTP', 'INFP', 'INFJ', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ']
const regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전남', '전북', '경북', '경남', '제주']

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/accounts/genres/')
    genres.value = res.data
  } catch (err) {
    console.error('장르 목록 불러오기 실패:', err)
  }
})

// ✅ 중복 방지 (computed)
const filteredGenresForSecond = computed(() => {
  return genres.value.filter(genre => genre.id !== firstGenre.value)
})
const filteredGenresForThird = computed(() => {
  return genres.value.filter(genre =>
    genre.id !== firstGenre.value && genre.id !== secondGenre.value
  )
})

const errorMsg = ref('')

// ✅ 회원가입 요청
const onRegister = async () => {
  // preferred_genres 리스트로 구성
  form.value.preferred_genres = [firstGenre.value, secondGenre.value, thirdGenre.value].filter(Boolean)

  if (form.value.preferred_genres.length === 0) {
    errorMsg.value = '선호 장르는 최소 1개 선택해야 합니다.'
    return
  }

  errorMsg.value = ''
  try {
    await userStore.register(form.value)
    router.push('/')
  } catch (error) {
    if (error.response?.data) {
      const errorData = error.response.data
      const firstKey = Object.keys(errorData)[0]
      errorMsg.value = `${firstKey}: ${errorData[firstKey]}`
    } else {
      errorMsg.value = '알 수 없는 오류가 발생하였습니다.'
    }
    alert(errorMsg.value)
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  min-height: 100vh;
}

.register-form {
  background: #1c1c1e;
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.form-title {
  color: #fff;
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  background: #2c2c2e;
  border: none;
  border-radius: 4px;
  color: #fff;
  outline: none;
}

.form-group input::placeholder {
  color: #bbb;
}

.form-group label {
  color: #fff;
  font-size: 0.9rem;
}

.submit-btn {
  width: 100%;
  background: #007aff;
  color: #fff;
  border: none;
  padding: 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.submit-btn:hover {
  background: #005fcc;
}

.error {
  color: #ff3b30;
  text-align: center;
  margin-top: 1rem;
}
</style>


