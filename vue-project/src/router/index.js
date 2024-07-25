import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import routes from '@/router/routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        auth: true
      }
    },
    {
      path: '/veiculo',
      name: 'cadastroVeiculo',
      component: () => import('@/views/VeiculoView.vue'),
      meta: {
        auth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      
    }
  ]
})

router.beforeEach(routes)

export default router
