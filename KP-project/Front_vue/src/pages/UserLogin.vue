<template>
  <div class="login-container">
    <h2>로그인</h2>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <form @submit.prevent="onLogIn">
      <div class="form-group">
        <label for="username">사용자 이름</label>
        <input id="username" v-model="username" class="form-control" @input="error = ''" />
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input id="password" v-model="password" type="password" class="form-control" @input="error = ''" />
      </div>

      <button type="submit" class="btn btn-primary w-100">로그인</button>
    </form>

    <p class="mt-3 text-muted text-center">
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
  if (!username.value.trim() || !password.value.trim()) {
    error.value = '아이디와 비밀번호를 모두 입력해주세요.'
    return
  }

  try {
    await userStore.logIn({ username: username.value, password: password.value })
    const nextRoute = router.currentRoute.value.query.next
    router.push(nextRoute || `/profile/${username.value}`)  // 프로필로 이동!
  } catch (err) {
    error.value = '로그인 실패. 정보를 확인하세요.'
    console.error(err)
  }
}
</script>

<style scoped>
/* 회원가입 페이지 스타일과 통일 */
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.login-container h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.login-container .form-group {
  margin-bottom: 1rem;
}

.login-container label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.login-container input[type="text"],
.login-container input[type="password"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.95rem;
}

.login-container button {
  margin-top: 0.5rem;
}

.login-container .text-muted {
  font-size: 0.9rem;
}
</style>

