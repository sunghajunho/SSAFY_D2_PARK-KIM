<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const currentPassword = ref('')
const newPassword = ref('')

const handleChangePassword = async () => {
  if (!currentPassword.value || !newPassword.value) {
    alert('모든 항목을 입력하세요.')
    return
  }
  await userStore.changePassword(currentPassword.value, newPassword.value)
  currentPassword.value = ''
  newPassword.value = ''
}
</script>

<template>
  <div class="change-password-container">
    <h2>비밀번호 변경</h2>
    <input v-model="currentPassword" type="password" placeholder="현재 비밀번호" />
    <input v-model="newPassword" type="password" placeholder="새 비밀번호" />
    <button @click="handleChangePassword">변경하기</button>
  </div>
</template>

<style scoped>
.change-password-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
input {
  display: block;
  width: 100%;
  margin: 8px 0;
  padding: 8px;
}
button {
  background: black;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
