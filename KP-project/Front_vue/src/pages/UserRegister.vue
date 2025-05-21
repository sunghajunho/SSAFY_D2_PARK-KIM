<template>
  <form @submit.prevent="onRegister">
    <!-- 기본 정보 입력 -->
    <label>Username:</label>
    <input type="text" v-model="form.username" />

    <label>Email:</label>
    <input type="email" v-model="form.email" />

    <label>Password:</label>
    <input type="password" v-model="form.password1" />

    <label>Password 확인:</label>
    <input type="password" v-model="form.password2" />

    <label>Real Name:</label>
    <input type="text" v-model="form.real_name" />

    <label>Nickname:</label>
    <input type="text" v-model="form.nickname" />

    <label>Age:</label>
    <input type="number" v-model.number="form.age" />

    <label>Gender:</label>
    <select v-model="form.gender">
      <option value="">선택</option>
      <option value="남성">남성</option>
      <option value="여성">여성</option>
    </select>

    <label>MBTI:</label>
    <select v-model="form.mbti">
      <option disabled value="">MBTI 선택</option>
      <option>INTP</option><option>INFP</option><option>INFJ</option><option>INTJ</option>
      <option>ISFP</option><option>ISFJ</option><option>ISTP</option><option>ISTJ</option>
      <option>ENFP</option><option>ENFJ</option><option>ENTP</option><option>ENTJ</option>
      <option>ESFP</option><option>ESFJ</option><option>ESTP</option><option>ESTJ</option>
    </select>

    <label>Region:</label>
    <select v-model="form.region">
      <option disabled value="">지역 선택</option>
      <option>서울</option><option>부산</option><option>대구</option><option>인천</option>
      <option>광주</option><option>대전</option><option>울산</option><option>세종</option>
      <option>경기</option><option>강원</option><option>충북</option><option>충남</option>
      <option>전남</option><option>전북</option><option>경북</option><option>경남</option><option>제주</option>
    </select>

    <!-- ✅ 선호 장르 체크박스 방식 -->
    <label>선호 장르 선택:</label>
    <div v-for="genre in genres" :key="genre.id">
      <input
        type="checkbox"
        :value="genre.id"
        v-model="form.preferred_genres"
      />
      {{ genre.name }}
    </div>

    <button type="submit">회원가입</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()

// ✅ 회원가입 폼 데이터
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
  preferred_genres: []
})

// ✅ 장르 목록 불러오기용 ref
const genres = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/accounts/genres/')
    genres.value = res.data
  } catch (err) {
    console.error('장르 목록 불러오기 실패:', err)
  }
})

// ✅ 회원가입 요청
const onRegister = async () => {
  await userStore.register(form.value)
}
</script>

