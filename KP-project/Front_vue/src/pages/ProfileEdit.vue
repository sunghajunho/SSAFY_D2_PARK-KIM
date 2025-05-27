<template>
  <div class="profile-edit-container">
    <h2>프로필 수정</h2>
    <form @submit.prevent="submitProfileUpdate" enctype="multipart/form-data">
      <div class="form-group">
        <label for="nickname">닉네임</label>
        <input id="nickname" v-model="nickname" type="text" placeholder="닉네임" />
      </div>

      <div class="form-group">
        <label for="age">나이</label>
        <input id="age" v-model="age" type="number" placeholder="나이" />
      </div>

      <div class="form-group">
        <label for="mbti">MBTI</label>
        <select id="mbti" v-model="mbti">
          <option disabled value="">선택해주세요</option>
          <option>INTJ</option><option>INTP</option><option>ENTJ</option><option>ENTP</option>
          <option>INFJ</option><option>INFP</option><option>ENFJ</option><option>ENFP</option>
          <option>ISTJ</option><option>ISFJ</option><option>ESTJ</option><option>ESFJ</option>
          <option>ISTP</option><option>ISFP</option><option>ESTP</option><option>ESFP</option>
        </select>
      </div>

      <div class="form-group">
        <label for="region">지역</label>
        <select id="region" v-model="region">
          <option disabled value="">선택해주세요</option>
          <option>서울</option><option>부산</option><option>대구</option>
          <option>인천</option><option>광주</option><option>대전</option>
          <option>울산</option><option>경기</option><option>강원</option>
          <option>충청</option><option>전라</option><option>경상</option><option>제주</option>
        </select>
      </div>

      <div class="form-group">
        <label>선호 장르 (1~3순위)</label>
        <div class="genre-priority">
          <label>1순위</label>
          <select v-model="firstPreferredGenre">
            <option disabled value="">선택해주세요</option>
            <option v-for="genre in genres" :key="genre.id" :value="genre.name" :disabled="isGenreSelected(genre.name, 1)">
              {{ genre.name }}
            </option>
          </select>

          <label>2순위</label>
          <select v-model="secondPreferredGenre">
            <option disabled value="">선택해주세요</option>
            <option v-for="genre in genres" :key="genre.id" :value="genre.name" :disabled="isGenreSelected(genre.name, 2)">
              {{ genre.name }}
            </option>
          </select>

          <label>3순위</label>
          <select v-model="thirdPreferredGenre">
            <option disabled value="">선택해주세요</option>
            <option v-for="genre in genres" :key="genre.id" :value="genre.name" :disabled="isGenreSelected(genre.name, 3)">
              {{ genre.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="profileImage">프로필 이미지</label>
        <input id="profileImage" type="file" @change="onFileChange" />
        <div v-if="previewImage" class="profile-preview">
          <p>미리보기:</p>
          <img :src="previewImage" alt="미리보기" width="100" height="100" />
          <button type="button" @click="deleteProfileImage" class="btn btn-danger mt-2">프로필 이미지 삭제</button>
        </div>
      </div>

      <button type="submit" class="btn btn-primary w-100">저장하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import axios from 'axios'
import api from '@/api/axios'

const userStore = useUserStore()
const genres = ref([])
const nickname = ref('')
const age = ref('')
const mbti = ref('')
const region = ref('')
const firstPreferredGenre = ref('')
const secondPreferredGenre = ref('')
const thirdPreferredGenre = ref('')
const profileImage = ref(null)
const previewImage = ref(null)

onMounted(async () => {
  const genreRes = await axios.get(api.defaults.baseURL + 'accounts/genres/')
  genres.value = genreRes.data

  const profileRes = await userStore.getUserProfile(userStore.username)
  nickname.value = profileRes.nickname
  age.value = profileRes.age
  mbti.value = profileRes.mbti
  region.value = profileRes.region

  // 선호 장르 기존값 세팅
  const existingGenres = profileRes.preferred_genres.map(g => g.name)
  firstPreferredGenre.value = existingGenres[0] || ''
  secondPreferredGenre.value = existingGenres[1] || ''
  thirdPreferredGenre.value = existingGenres[2] || ''

  const imagePath = profileRes.profile_image || '/media/default_profile.jpg'
  previewImage.value = (api.defaults.baseURL + imagePath).replace(/([^:]\/)\/+/g, '$1')
})

const isGenreSelected = (genreName, currentRank) => {
  if (currentRank !== 1 && genreName === firstPreferredGenre.value) return true
  if (currentRank !== 2 && genreName === secondPreferredGenre.value) return true
  if (currentRank !== 3 && genreName === thirdPreferredGenre.value) return true
  return false
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  profileImage.value = file
  if (file) {
    previewImage.value = URL.createObjectURL(file)
  }
}

const deleteProfileImage = async () => {
  try {
    await axios.delete(api.defaults.baseURL + 'accounts/profile/image/delete/', {
      headers: { Authorization: `Token ${userStore.token}` }
    })
    alert('프로필 이미지가 삭제되었습니다!')
    previewImage.value = (api.defaults.baseURL + '/media/default_profile.jpg').replace(/([^:]\/)\/+/g, '$1')
  } catch (err) {
    console.error(err)
    alert('프로필 이미지 삭제에 실패했습니다.')
  }
}

const submitProfileUpdate = async () => {
  const selectedGenres = [firstPreferredGenre.value, secondPreferredGenre.value, thirdPreferredGenre.value].filter(g => g !== '')
  const formData = new FormData()
  formData.append('nickname', nickname.value)
  formData.append('age', age.value)
  formData.append('mbti', mbti.value)
  formData.append('region', region.value)
  formData.append('preferred_genres', selectedGenres.join(','))
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }

  try {
    await userStore.updateProfile(formData)
    alert('프로필이 성공적으로 수정되었습니다!')
    window.location.href = `/profile/${userStore.username}`
  } catch (err) {
    console.error(err)
    alert('프로필 수정에 실패했습니다.')
  }
}
</script>

<style scoped>
/* 회원가입 페이지 스타일에 맞춘 스타일 */
.profile-edit-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.profile-edit-container h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.profile-edit-container .form-group {
  margin-bottom: 1rem;
}

.profile-edit-container label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.profile-edit-container input[type="text"],
.profile-edit-container input[type="number"],
.profile-edit-container input[type="file"],
.profile-edit-container select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.95rem;
}

.profile-edit-container .btn-danger {
  margin-top: 0.5rem;
  padding: 0.3rem 0.5rem;
  font-size: 0.9rem;
  border-radius: 5px;
}

.profile-edit-container img {
  margin-top: 0.5rem;
  border-radius: 50%;
  border: 1px solid #ddd;
}
</style>


