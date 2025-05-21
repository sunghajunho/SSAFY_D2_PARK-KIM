import { createRouter, createWebHistory } from 'vue-router'
import ArticleListView from '@/views/ArticleListView.vue'

const routes = [
  {
    path: '/',
    name: 'ArticleList',
    component: ArticleListView,
  },
  // 다른 라우트는 이후에 추가
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
