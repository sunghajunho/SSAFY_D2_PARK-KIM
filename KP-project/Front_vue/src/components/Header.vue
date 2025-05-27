<script setup>
import { useUserStore } from '@/stores/userStore'
import { useThemeStore } from '@/stores/themeStore'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.theme === 'dark')
const userStore = useUserStore()
const router = useRouter()

const logoutAndRedirect = async () => {
  await userStore.logout()
  router.replace('/')
}
</script>

<template>
  
  <nav class="navbar navbar-expand px-4" :class="isDark ? 'navbar-dark bg-dark' : 'navbar-light bg-light'">
    <router-link class="navbar-brand" to="/">MovieGPT</router-link>
    <div class="navbar-nav">
      <router-link class="nav-link" to="/search">영화 검색</router-link>
      <router-link class="nav-link" to="/reviews">리뷰</router-link>
      <router-link class="nav-link" to="/profile">내 프로필</router-link>
    </div>
    <div class="ms-auto d-flex align-items-center gap-3">
       <button
          class="btn btn-outline-secondary btn-icon"
          @click="themeStore.toggleTheme"
          title="테마 전환"
        >
          🌗
        </button>
      <span v-if="userStore.isLoggedIn">
  👋 {{ userStore.username }}
        <button @click="logoutAndRedirect" class="btn btn-sm btn-outline-danger ms-2">로그아웃</button>
      </span>
      <span v-else>
        <router-link to="/login" class="btn btn-sm btn-outline-primary me-2">로그인</router-link>
        <router-link to="/register" class="btn btn-sm btn-outline-success">회원가입</router-link>
      </span>
      </div>
  </nav>
</template>

<style scoped>
.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  padding: 0;
  font-size: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
  line-height: 1;
}
</style>a