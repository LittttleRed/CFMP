import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue'),
    meta: { 
      title: '用户登录',
    //   guestOnly: true // 标记仅未登录用户可访问
    }
  },
 {
  path: '/profile',
  name: 'Profile',
  component: () => import('../views/ProfilePage.vue'),
  meta: { requiresAuth: true }
}
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

export default router