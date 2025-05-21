<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

function handleRegister() {
  if (!username.value || !password.value) {
    error.value = '모든 항목을 입력하세요'
    return
  }

  userStore.register(username.value, password.value)
  router.push('/login')
}
</script>

<template>
  <div class="container mt-5">
    <h2>회원가입</h2>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <form @submit.prevent="handleRegister">
      <div class="mb-3">
        <label class="form-label">사용자 이름</label>
        <input v-model="username" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">비밀번호</label>
        <input v-model="password" type="password" class="form-control" />
      </div>
      <button class="btn btn-primary">가입하기</button>
    </form>
  </div>
</template>
