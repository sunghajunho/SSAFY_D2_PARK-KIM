<script setup>
import { computed, onMounted,ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useReviewStore } from '@/stores/reviewStore'
import { useRoute } from 'vue-router'

const route = useRoute()
const userStore = useUserStore()
const reviewStore = useReviewStore()

const profile = ref('')
const usernameParam = route.params.username

const fetchProfile = async () => {
  if (usernameParam) {
    profile.value = await userStore.getUserProfile(usernameParam)
  } else  {
    // 내 프로필
    await userStore.fetchUserInfo()
    profile.value = {
      username: userStore.username,
      nickname: userStore.nickname
    }
  }
}

onMounted(() => {
  fetchProfile()
})

// ✅ 반응형 computed로 필터링
const myReviews = computed(() =>
  reviewStore.getReviewsByAuthor(profile.value?.username)
)

const myComments = computed(() =>
  reviewStore.comments.filter(c => c.author?.username === profile.value?.username)
)
</script>

<template>
  <div class="container mt-5">
    <h2 class="mb-3">👤 {{ usernameParam ? profile.nickname + '의 프로필' : '내 프로필' }}</h2>
    <p class="text-muted">사용자명: <strong>{{ profile.username }}</strong></p>

    <hr />

    <h4 class="mt-4">내가 쓴 리뷰</h4>
    <ul v-if="myReviews.length" class="list-group mb-4">
      <li v-for="review in myReviews" :key="review.id" class="list-group-item">
        {{ review.title }} ({{ review.createdAt }})
      </li>
    </ul>
    <p v-else class="text-muted">작성한 리뷰가 없습니다.</p>

    <h4 class="mt-4">내가 단 댓글</h4>
    <ul v-if="myComments.length" class="list-group">
      <li v-for="comment in myComments" :key="comment.id" class="list-group-item">
        {{ comment.content }} ({{ comment.createdAt }})
      </li>
    </ul>
    <p v-else class="text-muted">작성한 댓글이 없습니다.</p>
  </div>
</template>

