<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <h2 class="mb-4 text-center">🎬 영화 취향을 입력해보세요</h2>
        <div class="input-group">
          <input
            v-model="query"
            @keydown.enter="handleSearch"
            type="text"
            class="form-control"
            placeholder="예: 액션, 해피엔딩, 눈물나는 영화"
          />
          <button class="btn btn-primary" @click="handleSearch">검색</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      query: '',
    }
  },
  methods: {
    handleSearch() {
      if (!this.query.trim()) return
      this.$router.push({ name: 'Results', query: { q: this.query } })
    },
  },
}
</script>
