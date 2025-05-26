<script setup>
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useReviewStore } from '@/stores/reviewStore'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const reviewStore = useReviewStore()

const profile = ref({})
const usernameParam = route.params.username

const fetchProfile = async () => {
  if (usernameParam) {
    profile.value = await userStore.getUserProfile(usernameParam)
  } else {
    profile.value = await userStore.getUserProfile(userStore.username)
  }
}

// ✅ 중복된 슬래시 문제를 해결해서 전체 URL 생성
const profileImageURL = computed(() => {
  const imagePath = profile.value.profile_image || '/media/default_profile.jpg'
  return (api.defaults.baseURL + imagePath).replace(/([^:]\/)\/+/g, '$1')
})

const isMyProfile = computed(() => {
  return !usernameParam || usernameParam === userStore.username
})

const isFollowing = ref(false)
const followers = ref([])
const following = ref([])
const showFollowers = ref(false)
const showFollowing = ref(false)

const handleFollowToggle = async () => {
  const status = await userStore.toggleFollow(profile.value.id)
  isFollowing.value = status === 'followed'
  followers.value = await userStore.getFollowers(usernameParam)
}

const goToFollowers = () => {
  router.push(`/profile/${profile.value.username}/followers`)
}

const goToFollowing = () => {
  router.push(`/profile/${profile.value.username}/following`)
}

onMounted(() => {
  fetchProfile()
})

// ✅ 반응형 computed로 내 리뷰, 댓글 필터링
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
    
    <!-- ✅ 최종 정리된 profileImageURL 사용 -->
    <img :src="profileImageURL" alt="프로필 이미지" width="150" height="150" />
    
    <p class="text-muted">사용자명: <strong>{{ profile.username }}</strong></p>
    <h3>{{ profile.nickname }} ({{ profile.username }})</h3>
    
    <div v-if="isMyProfile">
      <router-link to="/profile/edit" class="btn btn-primary">프로필 변경</router-link>
    </div>
    
    <button @click="handleFollowToggle">
      {{ isFollowing ? '팔로우 취소' : '팔로우' }}
    </button>

    <div>
      <span @click="goToFollowers">팔로워: {{ followers.length }}</span>
      <span @click="goToFollowing">팔로잉: {{ following.length }}</span>
    </div>

    <div v-if="showFollowers">
      <h4>팔로워</h4>
      <ul>
        <li v-for="follower in followers" :key="follower">
          <router-link :to="`/profile/${follower}`">{{ follower }}</router-link>
        </li>
      </ul>
    </div>

    <div v-if="showFollowing">
      <h4>팔로잉</h4>
      <ul>
        <li v-for="user in following" :key="user">
          <router-link :to="`/profile/${user}`">{{ user }}</router-link>
        </li>
      </ul>
    </div>

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
