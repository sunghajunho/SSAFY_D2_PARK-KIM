<script setup>
import { ref, onMounted,computed } from 'vue'
import { useReviewStore } from '@/stores/reviewStore'
import { useUserStore } from '@/stores/userStore'

const props = defineProps({
  reviewId: {
    type: Number,
    required: true,
  },
})

const store = useReviewStore()
const userStore = useUserStore()

const newComment = ref('')
const replyText = ref('')
const replyingTo = ref(null)

const editingCommentId = ref(null)
const editBuffer = ref('')

async function loadComments() {
  await store.fetchComments(props.reviewId)
}

function submitComment() {
  if (!newComment.value.trim()) return
  store.addComment(props.reviewId, newComment.value)
  newComment.value = ''
}

function submitReply(parentId) {
  if (!replyText.value.trim()) return
  store.addComment(props.reviewId, replyText.value, parentId)
  replyText.value = ''
  replyingTo.value = null
}

function toggleReply(id) {
  replyingTo.value = replyingTo.value === id ? null : id
}

function startEdit(comment) {
  editingCommentId.value = comment.id
  editBuffer.value = comment.content
}

function cancelEdit() {
  editingCommentId.value = null
  editBuffer.value = ''
}

function submitEdit(articleId,commentId) {
  store.updateComment(articleId,commentId, editBuffer.value)
  cancelEdit()
}

function handleDelete(articleId,commentId) {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    store.deleteComment(articleId,commentId)
  }
}

function handleCommentLike(commentId) {
  store.toggleCommentLike(props.reviewId, commentId)
}

onMounted(() => {
  loadComments()
})

// ✅ 정렬된 댓글 계산
const sortedComments = computed(() => {
  return [...store.getCommentsByReviewId(props.reviewId)]
    .sort((a, b) => {
      if (b.comment_likes === a.comment_likes) {
        // 좋아요 수가 같으면 created_at이 빠른 순서
        return new Date(a.created_at) - new Date(b.created_at)
      }
      return b.comment_likes - a.comment_likes
    })
})
</script>

<template>
  <div class="mb-4">
    <!-- 댓글 입력 -->
    <form @submit.prevent="submitComment" class="mb-3">
      <textarea
        v-model="newComment"
        class="form-control mb-2"
        rows="2"
        placeholder="댓글 작성"
        :disabled="!userStore.isLoggedIn"
      ></textarea>
      <button class="btn btn-sm btn-primary" :disabled="!userStore.isLoggedIn">작성</button>
    </form>

    <!-- 댓글 리스트 -->
           <!-- v-for="comment in store.getCommentsByReviewId(props.reviewId)" -->
    <div
      v-for="comment in sortedComments"
      :key="comment.id"
      class="mb-3"
    >
      <div class="p-2 bg-light border rounded">
        <p class="mb-1">{{ comment.content }}</p>
        <small class="text-muted">
          {{ comment.author.nickname }} · {{ comment.created_at }}
        </small>

        <button @click="handleCommentLike(comment.id)">
          {{ comment.is_liked ? '💔' : '❤️' }} {{ comment.comment_likes }}
        </button>
        
        <div class="mt-2">
          <a href="#" @click.prevent="toggleReply(comment.id)">💬 답글</a>
          <template v-if="comment.author.username === userStore.username">
            <a href="#" @click.prevent="startEdit(comment)">✏️ 수정</a>
            <a href="#" @click.prevent="handleDelete(props.reviewId,comment.id)">🗑 삭제</a>
          </template>
          <!-- 수정 폼 -->
          <div v-if="editingCommentId === comment.id" class="mt-2">
            <textarea v-model="editBuffer" class="form-control mb-2" rows="2"></textarea>
            <button class="btn btn-sm btn-primary" @click="submitEdit(props.reviewId,comment.id)">저장</button>
            <button class="btn btn-sm btn-secondary ms-2" @click="cancelEdit">취소</button>
          </div>
        </div>

        <!-- 대댓글 입력창 -->
        <div v-if="replyingTo === comment.id" class="mt-2">
          <textarea
            v-model="replyText"
            class="form-control mb-2"
            rows="2"
            placeholder="답글 작성"
          ></textarea>
          <button class="btn btn-sm btn-secondary" @click="submitReply(comment.id)">
            답글 등록
          </button>
        </div>

        <!-- 대댓글 리스트 -->
        <div
          v-if="store.getReplies(comment.id).length"
          class="mt-3 ps-4 border-start"
        >
          <div
            v-for="reply in store.getReplies(comment.id)"
            :key="reply.id"
            class="p-2 bg-white border rounded mb-2"
          >
            <p class="mb-1">{{ reply.content }}</p>
            <small class="text-muted">
              {{ reply.author.nickname }} · {{ reply.created_at }}
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
