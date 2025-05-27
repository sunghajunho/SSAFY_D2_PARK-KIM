<template>
  <div class="preference-match">
    <div class="match-info">
      <span>취향매칭률</span>
      <span class="match-rate">{{ matchRate }}%</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// ⭐ 실제로는 API를 통해 불러오거나 props로 전달받을 수 있어
const matchRate = ref(26)

onMounted(() => {
  // API 호출해서 matchRate.value 업데이트 가능!
})
</script>

<style scoped>
.preference-match {
  display: flex;
  align-items: center;
  justify-content: center;  /* 🔥 텍스트를 가운데 정렬! */
  background-color: #f9f9f9; /* 💡 박스 배경색 (선택) */
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 1rem;
  font-weight: bold; /* 🔥 전체 글자를 볼드체로! */
  box-sizing: border-box; /* ✅ 박스 내부 여백 포함 */
}

.match-info {
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
