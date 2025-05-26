<template>
  <div class="followers-list">
    <h3 class="text-lg font-semibold mb-4">{{ username }}님의 팔로워 목록</h3>
    <ul>
      <li
        v-for="follower in followers"
        :key="follower"
        class="mb-1 text-blue-500 hover:underline cursor-pointer"
      >
        <router-link :to="`/profile/${follower}`">{{ follower }}</router-link>
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
const followers = ref([])

const fetchFollowers = async () => {
  try {
    followers.value = await userStore.getFollowers(username)
  } catch (err) {
    console.error('팔로워 조회 실패:', err)
  }
}

onMounted(() => {
  fetchFollowers()
})
</script>

<style scoped>
.followers-list {
  max-width: 500px;
  margin: auto;
  padding: 1rem;
}
</style>
