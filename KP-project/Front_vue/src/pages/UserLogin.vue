<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

function handleLogin() {
  const success = userStore.login(username.value, password.value)
  if (!success) {
    error.value = '로그인 실패. 정보를 확인하세요.'
  } else {
    router.push('/profile')
  }
}
</script>

<template>
  <div class="container mt-5">
    <h2>로그인</h2>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label class="form-label">사용자 이름</label>
        <input v-model="username" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">비밀번호</label>
        <input v-model="password" type="password" class="form-control" />
      </div>
      <button class="btn btn-success">로그인</button>
    </form>
      <p class="mt-3 text-muted">
      아직 회원이 아니신가요?
      <router-link to="/register" class="ms-1">회원가입</router-link>
      </p>
  </div>
</template>
