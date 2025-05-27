import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

import Home from '@/pages/Home.vue'
import Results from '@/pages/Results.vue'
import Detail from '@/pages/Detail.vue'
import ReviewBoard from '@/pages/ReviewBoard.vue'
import ReviewDetail from '@/pages/ReviewDetail.vue'
import UserLogin from '@/pages/UserLogin.vue'
import ChangePassword from '@/pages/ChangePassword.vue'
import UserRegister from '@/pages/UserRegister.vue'
import UserProfile from '@/pages/UserProfile.vue'
import ProfileEdit from '@/pages/ProfileEdit.vue'
import ReviewCreatePage from '@/pages/ReviewCreatePage.vue'
import FollowersList from '@/pages/FollowersList.vue'
import FollowingList from '@/pages/FollowingList.vue'
import ProfilePosts from '@/pages/ProfilePosts.vue'
import ProfileComments from '@/pages/ProfileComments.vue'
import Search from '@/pages/Search.vue'  // ← 이 줄 추가
import MovieArticlesBoard from '@/pages/MovieArticlesBoard.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/results', name: 'Results', component: Results },
  { path: '/detail/:id', name: 'Detail', component: Detail, props: true },
  { path: '/reviews', name: 'ReviewBoard', component: ReviewBoard },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  { path: '/register', name: 'UserRegister', component: UserRegister },
  { path: '/profile/change-password', name:'ChangePassword',component: ChangePassword},
  { path: '/profile', name: 'MyProfile', component: UserProfile, meta: { requiresAuth: true }},
  { path: '/profile/:username', name: 'UserProfile', component: UserProfile, meta: { requiresAuth: true } },
  { path: '/profile/:username/posts', name: 'ProfilePosts', component: ProfilePosts},
  { path: '/profile/:username/comments', name: 'ProfileComments', component: ProfileComments},
  { path: '/profile/edit', name: 'ProfileEdit', component: ProfileEdit, meta: {requiresAuth: true}},
  { path: '/reviews/write', name: 'ReviewWrite', component: ReviewCreatePage, meta: { requiresAuth: true } },
  { path: '/reviews/:id', name: 'ReviewDetail', component: ReviewDetail },
  { path: '/profile/:username/followers', name : 'FollowersList', component: FollowersList},
  { path: '/profile/:username/following', name : 'FollowingList', component: FollowingList},
  { path: '/search', name : 'Search', component: Search},
  { path: '/movies/:id/articles', name: 'MovieArticlesBoard', component: MovieArticlesBoard},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.token) {
    alert('로그인이 필요합니다.')
    next({
      name: 'UserLogin',
      query: { next: to.fullPath } // 👈 원래 보려던 페이지 기억
    })
  } else {
    next()
  }
})
