<script setup>
import { useUserStore } from '@/stores/userStore'
const userStore = useUserStore()
</script>

<template>
  <nav class="navbar navbar-expand navbar-light bg-light px-4">
    <router-link class="navbar-brand" to="/">MovieGPT</router-link>
    <div class="navbar-nav">
      <router-link class="nav-link" to="/reviews">리뷰</router-link>
      <router-link class="nav-link" to="/profile">내 프로필</router-link>
    </div>
    <div class="ms-auto">
      <span v-if="userStore.isLoggedIn">
        👋 {{ userStore.username }}
        <button @click="userStore.logout" class="btn btn-sm btn-outline-danger ms-2">로그아웃</button>
      </span>
      <span v-else>
        <router-link to="/login" class="btn btn-sm btn-outline-primary me-2">로그인</router-link>
        <router-link to="/register" class="btn btn-sm btn-outline-success">회원가입</router-link>
        </span>
    </div>
  </nav>
</template>