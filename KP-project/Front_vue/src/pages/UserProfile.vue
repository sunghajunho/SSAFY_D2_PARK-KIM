<script setup>
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useReviewStore } from '@/stores/reviewStore'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import ProfileFavorites from '@/components/ProfileFavorites.vue'
import Wordcloud from '@/components/Wordcloud.vue' 

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const reviewStore = useReviewStore()

const profile = ref({})
const usernameParam = route.params.username

const showMenu = ref(false)

const toggleMenu = () => {
  showMenu.value = !showMenu.value
  console.log(showMenu.value)
}

const fetchProfile = async () => {
  if (usernameParam) {
    profile.value = await userStore.getUserProfile(usernameParam)
    console.log(profile.value)
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

onMounted(async () => {
  await fetchProfile()
  await reviewStore.fetchUserReviews(usernameParam || userStore.username)
  await reviewStore.fetchUserComments(usernameParam || userStore.username)
  followers.value = await userStore.getFollowers(usernameParam || userStore.username)
  following.value = await userStore.getFollowing(usernameParam || userStore.username)
})

// ✅ 반응형 computed로 내 리뷰, 댓글 필터링
const myReviews = computed(() =>
  reviewStore.getReviewsByAuthor(profile.value?.username)
)

const myComments = computed(() =>
  reviewStore.comments.filter(c => c.author?.username === profile.value?.username)
)

const handleDeleteAccount = async () => {
  if (confirm('정말로 탈퇴하시겠습니까?')) {
    await userStore.deleteUserAccount()
  }
}

const goToEditProfile = () => {
  router.push('/profile/edit')
}

const goToChangePassword = () => {
  router.push('/profile/change-password')
}
</script>

<template>
  <div>
    <div class="profile-container">
      <div class="profile-header">
        <img :src="profileImageURL" alt="프로필 사진" class="profile-image" />
        <div class="profile-info">
          <h2>{{ profile.nickname }}</h2>
          <div class="follow-info">
            <router-link :to="`/profile/${profile.username}/followers`" class="follow-link">
              <span>팔로워 <b>{{ followers.length }}</b> | </span>
            </router-link>
            |
            <router-link :to="`/profile/${profile.username}/following`" class="follow-link">
              <span>팔로잉 <b>{{ following.length }}</b></span>
            </router-link>
          </div>
          <div v-if="isMyProfile">
            <router-link to="/profile/edit" class="edit-profile-btn">  ✏️ </router-link>
          </div>
        </div>

        <div class="dropdown-container">
          <button class="gear-icon" @click="toggleMenu">⚙️</button>
            <div v-if="showMenu.value" class="dropdown-menu">
              <button @click="goToEditProfile">회원정보 수정</button>
              <button @click="goToChangePassword">비밀번호 변경</button>
              <button @click="handleDeleteAccount" class="delete-btn">회원탈퇴</button>
            </div>
        </div>
      </div>

      <div class="follow-btn-container">
        <button @click="handleFollowToggle" class="follow-btn">
          {{ isFollowing ? '팔로우 취소' : '팔로우' }}
        </button>
      </div>

      <div class="profile-stats">
        <div class="stat">
          <router-link :to="`/profile/${profile.username}/posts`" class="stat-link">
              <span class="stat-number">{{ myReviews.length }}</span>
              <span class="stat-label">게시글</span>
          </router-link>
        </div>

        <div class="stat">
          <router-link :to="`/profile/${profile.username}/comments`" class="stat-link">
              <span class="stat-number">{{ myComments.length }}</span>
              <span class="stat-label">댓글</span>
          </router-link>
        </div>

        <div class="stat">
            <span class="stat-number">0</span>
            <span class="stat-label">컬렉션</span>
          </div>
      </div>
    </div>

    <hr />

    <Wordcloud />

    <hr />

    <ProfileFavorites :is-my-profile="isMyProfile"/>


  </div>
</template>

<style scoped>
/* 전체 컨테이너를 중앙 정렬 + 고정 폭 */
.profile-container {
  width: 760px; /* 적당한 너비 */
  margin: 0 auto;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* 프로필 헤더 */
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 20px;
}

.profile-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
}

.profile-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: center;
}

.user-name {
  margin: 0;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
}

.badge {
  margin-left: 6px;
  font-size: 1rem;
  color: red;
}

.follow-info {
  display: flex;
  flex-direction: row;
  gap: 4px;
  font-size: 0.9rem;
  color: #555;
  margin-top: 8px;
}

.follow-info b {
  font-weight: bold;
  color: #000;
}

.bio {
  margin: 0;
  font-size: 0.9rem;
  color: #555;
}

.edit-profile-btn {
  position: absolute;
  top: 10px;       /* 위쪽 여백 */
  right: 10px;     /* 오른쪽 여백 */
  background: none; /* 배경 없앰 */
  border: none;     /* 테두리 없앰 */
  font-size: 1.2rem; /* 아이콘 크기 조정 */
  cursor: pointer;
  color: #333;
}

.edit-profile-btn:hover {
  color: #000;     /* 호버 시 색 변경 */
}

/* 팔로우 버튼 영역 */
.follow-btn-container {
  border-top: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

.follow-btn {
  background-color: black;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 0;
  width: 100%;
  font-size: 1rem;
  cursor: pointer;
}

/* ✅ 게시글/댓글/컬렉션 통계 스타일 */
.profile-stats {
  display: flex;
  border-top: 1px solid #ddd;
  padding: 12px 0;
}

.stat {
  flex: 1;
  text-align: center;
}

.stat-link {
  text-decoration: none;
  color: inherit;
}

.stat-number {
  font-size: 1.2rem;
  font-weight: bold;
}

.stat-label {
  display: flex;
  flex-direction: column;
  font-size: 0.8rem;
  color: #777;
}

.dropdown-container {
  position: relative;
  display: inline-block;
}

.gear-icon {
  font-size: 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
}

.dropdown-menu {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 120%;
  right: 0;
  min-width: 140px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.dropdown-menu button {
  padding: 10px 12px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
}

.dropdown-menu button:hover {
  background: #f5f5f5;
}

.delete-btn {
  color: red;
}
</style>