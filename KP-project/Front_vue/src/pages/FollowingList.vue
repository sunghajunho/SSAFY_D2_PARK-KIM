<template>
  <div class="following-list">
    <h3 class="text-lg font-semibold mb-4">{{ username }}님의 팔로잉 목록</h3>
    <ul>
      <li
        v-for="user in following"
        :key="user"
        class="mb-1 text-blue-500 hover:underline cursor-pointer"
      >
        <router-link :to="`/profile/${user}`">{{ user }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const route = useRoute()
const userStore = useUserStore()
const username = route.params.username
const following = ref([])

const fetchFollowing = async () => {
  try {
    following.value = await userStore.getFollowing(username)
  } catch (err) {
    console.error('팔로잉 조회 실패:', err)
  }
}

onMounted(() => {
  fetchFollowing()
})
</script>

<style scoped>
.following-list {
  max-width: 500px;
  margin: auto;
  padding: 1rem;
}
</style>

