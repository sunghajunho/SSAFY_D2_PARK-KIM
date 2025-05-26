<template>
  <div class="profile-edit">
    <h2>프로필 수정</h2>
    <form @submit.prevent="submitProfileUpdate" enctype="multipart/form-data">
      <div>
        <label>닉네임</label>
        <input v-model="nickname" placeholder="닉네임" />
      </div>

      <div>
        <label>나이</label>
        <input v-model="age" type="number" placeholder="나이" />
      </div>

      <div>
        <label>MBTI</label>
        <select v-model="mbti">
          <option disabled value="">선택해주세요</option>
          <option>INTJ</option><option>INTP</option><option>ENTJ</option><option>ENTP</option>
          <option>INFJ</option><option>INFP</option><option>ENFJ</option><option>ENFP</option>
          <option>ISTJ</option><option>ISFJ</option><option>ESTJ</option><option>ESFJ</option>
          <option>ISTP</option><option>ISFP</option><option>ESTP</option><option>ESFP</option>
        </select>
      </div>

      <div>
        <label>지역</label>
        <select v-model="region">
          <option disabled value="">선택해주세요</option>
          <option>서울</option><option>부산</option><option>대구</option>
          <option>인천</option><option>광주</option><option>대전</option>
          <option>울산</option><option>경기</option><option>강원</option>
          <option>충청</option><option>전라</option><option>경상</option><option>제주</option>
        </select>
      </div>

      <div>
        <label>선호 장르</label>
        <div v-for="genre in genres" :key="genre.id" class="genre-item">
          <label>
            <input type="checkbox" :value="genre.name" v-model="preferredGenres" />
            {{ genre.name }}
          </label>
        </div>
      </div>

      <div>
        <label>프로필 이미지</label>
        <input type="file" @change="onFileChange" />
        <div v-if="previewImage">
          <p>미리보기:</p>
          <img :src="previewImage" alt="미리보기" width="100" height="100" />
          <button type="button" @click="deleteProfileImage" class="btn btn-danger mt-2">프로필 이미지 삭제</button>
        </div>
      </div>

      <button type="submit">저장하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import axios from 'axios'
import api from '@/api/axios' // ✅ baseURL 가져오기

const userStore = useUserStore()
const genres = ref([])
const nickname = ref('')
const age = ref('')
const mbti = ref('')
const region = ref('')
const preferredGenres = ref([])
const profileImage = ref(null)
const previewImage = ref(null)

onMounted(async () => {
  // ✅ 장르 목록 가져오기
  const genreRes = await axios.get(api.defaults.baseURL + 'accounts/genres/')
  genres.value = genreRes.data

  // ✅ 기존 프로필 정보 불러오기
  const profileRes = await userStore.getUserProfile(userStore.username)
  nickname.value = profileRes.nickname
  age.value = profileRes.age
  mbti.value = profileRes.mbti
  region.value = profileRes.region
  preferredGenres.value = profileRes.preferred_genres.map(g => g.name)

  // ✅ 프로필 이미지 경로 완성
  const imagePath = profileRes.profile_image || '/media/default_profile.jpg'
  previewImage.value = (api.defaults.baseURL + imagePath).replace(/([^:]\/)\/+/g, '$1')
})

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
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    alert('프로필 이미지가 삭제되었습니다!')
    // 미리보기도 기본 이미지로 다시 설정
    previewImage.value = (api.defaults.baseURL + '/media/default_profile.jpg').replace(/([^:]\/)\/+/g, '$1')
  } catch (err) {
    console.error('프로필 이미지 삭제 실패:', err)
    alert('프로필 이미지 삭제에 실패했습니다.')
  }
}

const submitProfileUpdate = async () => {
  const formData = new FormData()
  formData.append('nickname', nickname.value)
  formData.append('age', age.value)
  formData.append('mbti', mbti.value)
  formData.append('region', region.value)
  formData.append('preferred_genres', preferredGenres.value.join(','))
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }

  try {
    await userStore.updateProfile(formData)
    alert('프로필이 성공적으로 수정되었습니다!')
    location.reload()
  } catch (err) {
    console.error(err)
    alert('프로필 수정에 실패했습니다.')
  }
}
</script>

<style scoped>
.profile-edit {
  max-width: 400px;
  margin: 0 auto;
}
.profile-edit form div {
  margin-bottom: 10px;
}
.genre-item {
  margin-bottom: 5px;
}
</style>

