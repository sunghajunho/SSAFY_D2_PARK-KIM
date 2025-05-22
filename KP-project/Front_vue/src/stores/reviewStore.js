// src/stores/reviewStore.js
import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useReviewStore = defineStore('review', {
  state: () => ({
    reviews: [],
    currentReview: null,
    comments: [],
  }),

  actions: {
    async fetchReviews() {
      try {
        const res = await api.get('/community/articles/')
        this.reviews = res.data
      } catch (e) {
        console.error('리뷰 리스트 불러오기 실패', e)
      }
    },

    async fetchReview(id) {
      try {
        const res = await api.get(`/community/articles/${id}/`)
        this.currentReview = res.data
      } catch (e) {
        console.error('리뷰 상세 불러오기 실패', e)
      }
    },

    async createReview(data) {
      try {
        const res = await api.post('/community/articles/', data)
        this.reviews.unshift(res.data)
        return res.data.id
      } catch (e) {
        console.error('리뷰 작성 실패', e.response?.data || e)
        return null
      }
    },

    async updateReview(id, data) {
      try {
        const res = await api.put(`/community/articles/${id}/`, data)
        this.currentReview = res.data
        this.reviews = this.reviews.map((r) =>
          r.id === id ? res.data : r
        )
      } catch (e) {
        console.error('리뷰 수정 실패', e)
      }
    },

    async deleteReview(id) {
      try {
        await api.delete(`/community/articles/${id}/`)
        this.reviews = this.reviews.filter((r) => r.id !== id)
      } catch (e) {
        console.error('리뷰 삭제 실패', e)
      }
    },

    // ===== 댓글 =====
    async fetchComments(reviewId) {
      try {
        const res = await api.get(`/community/articles/${reviewId}/comments/`)
        this.comments = res.data
      } catch (e) {
        console.error('댓글 로딩 실패', e)
      }
    },

    async addComment(reviewId, content, parentId = null) {
      try {
        const res = await api.post('/community/comments/', {
          article: reviewId,
          content,
          parent: parentId,
        })
        this.comments.push(res.data)
      } catch (e) {
        console.error('댓글 작성 실패', e)
      }
    },

    async updateComment(commentId, content) {
      try {
        const res = await api.put(`/community/comments/${commentId}/`, {
          content,
        })
        this.comments = this.comments.map((c) =>
          c.id === commentId ? res.data : c
        )
      } catch (e) {
        console.error('댓글 수정 실패', e)
      }
    },

    async deleteComment(commentId) {
      try {
        await api.delete(`/community/comments/${commentId}/`)
        this.comments = this.comments.filter((c) => c.id !== commentId)
      } catch (e) {
        console.error('댓글 삭제 실패', e)
      }
    },

    getCommentsByReviewId(reviewId) {
      return this.comments.filter((c) => c.article === reviewId && c.parent === null)
    },

    getReplies(parentId) {
      return this.comments.filter((c) => c.parent === parentId)
    },

    // ⭐ 작성자 기준 리뷰 필터링
    getReviewsByAuthor(authorUsername) {
      return this.reviews.filter((r) => r.author.username === authorUsername)
    },
  },
})
