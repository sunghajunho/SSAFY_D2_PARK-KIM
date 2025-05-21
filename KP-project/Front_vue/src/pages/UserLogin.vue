<template>
  <div class="container mt-5">
    <h2>로그인</h2>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <form @submit.prevent="onLogIn">
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

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

const onLogIn = async () => {
  try {
    await userStore.logIn({ username: username.value, password: password.value })
    router.push('/profile')
  } catch (err) {
    error.value = '로그인 실패. 정보를 확인하세요.'
    console.error(err)
  }
}
</script>
