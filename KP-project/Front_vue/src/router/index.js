import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Results from '@/pages/Results.vue'
import Detail from '@/pages/Detail.vue'

import ReviewBoard from '@/pages/ReviewBoard.vue'
import ReviewDetail from '@/pages/ReviewDetail.vue'
import UserLogin from '@/pages/UserLogin.vue'
import UserRegister from '@/pages/UserRegister.vue'
import UserProfile from '@/pages/UserProfile.vue'
import ReviewCreatePage from '@/pages/ReviewCreatePage.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/results', name: 'Results', component: Results },
  { path: '/detail/:id', name: 'Detail', component: Detail, props: true },
  { path: '/reviews', name: 'ReviewBoard', component: ReviewBoard },
  { path: '/reviews/write', name: 'ReviewWrite', component: ReviewCreatePage },
  { path: '/reviews/:id', name: 'ReviewDetail', component: ReviewDetail },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  { path: '/register', name: 'UserRegister', component: UserRegister },
  { path: '/profile', name: 'UserProfile', component: UserProfile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
