import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: () => import('../views/Dashboard.vue'), name: 'Dashboard' },
  { path: '/models', component: () => import('../views/Models.vue'), name: 'Models' },
  { path: '/tasks', component: () => import('../views/Tasks.vue'), name: 'Tasks' },
  { path: '/leaderboard', component: () => import('../views/Leaderboard.vue'), name: 'Leaderboard' },
  { path: '/battles/:id', component: () => import('../views/BattleDetail.vue'), name: 'BattleDetail' },
  { path: '/reports', component: () => import('../views/Reports.vue'), name: 'Reports' },
  { path: '/system', component: () => import('../views/System.vue'), name: 'System' },
]

export default createRouter({ history: createWebHistory(), routes })
