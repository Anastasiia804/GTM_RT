import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Advertisers from '../views/Advertisers.vue'
import AdvertiserDetail from '../views/AdvertiserDetail.vue'
import Scripts from '../views/Scripts.vue'
import Health from '../views/Health.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/advertisers',
    name: 'Advertisers',
    component: Advertisers
  },
  {
    path: '/advertisers/:id',
    name: 'AdvertiserDetail',
    component: AdvertiserDetail
  },
  {
    path: '/scripts',
    name: 'Scripts',
    component: Scripts
  },
  {
    path: '/health',
    name: 'Health',
    component: Health
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
