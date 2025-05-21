<template>
  <form @submit.prevent="onRegister">
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
      <option>INTP</option>
      <option>INFP</option>
      <option>INFJ</option>
      <option>INTJ</option>
      <option>ISFP</option>
      <option>ISFJ</option>
      <option>ISTP</option>
      <option>ISTJ</option>
      <option>ENFP</option>
      <option>ENFJ</option>
      <option>ENTP</option>
      <option>ENTJ</option>
      <option>ESFP</option>
      <option>ESFJ</option>
      <option>ESTP</option>
      <option>ESTJ</option>
    </select>

    <label>Region:</label>
    <select v-model="form.region">
      <option disabled value="">지역 선택</option>
      <option>서울</option>
      <option>부산</option>
      <option>대구</option>
      <option>인천</option>
      <option>광주</option>
      <option>대전</option>
      <option>울산</option>
      <option>세종</option>
      <option>경기</option>
      <option>강원</option>
      <option>충북</option>
      <option>충남</option>
      <option>전남</option>
      <option>전북</option>
      <option>경북</option>
      <option>경남</option>
      <option>제주</option>
    </select>

    <label>선호 장르 ID 목록 (예: 1,2,3):</label>
    <input v-model="genreInput" placeholder="장르 ID 쉼표로 입력" />

    <button type="submit">회원가입</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()

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

const genreInput = ref('')

const onRegister = async () => {
  form.value.preferred_genres = genreInput.value
    .split(',')
    .map(str => parseInt(str.trim()))
    .filter(id => !isNaN(id))

  await userStore.register(form.value)
}
</script>
