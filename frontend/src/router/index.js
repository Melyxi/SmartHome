import { createRouter, createWebHistory } from 'vue-router';
import MainDashboard from '../components/Dashboard.vue';

const routes = [
  {
    path: '/',
    name: 'MainDashboard',
    component: MainDashboard,
  },
  // Добавьте другие маршруты...
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;