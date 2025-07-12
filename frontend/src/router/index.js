import { createRouter, createWebHistory } from 'vue-router';

const Login = () => import('../views/Login.vue');
const Signup = () => import('../views/Signup.vue');
const UserDashboard = () => import('../views/UserDashboard.vue');
const BookSpot = () => import('../views/BookSpot.vue');
const ReleaseSpot = () => import('../views/ReleaseSpot.vue');
const AdminDashboard = () => import('../views/AdminDashboard.vue');
const CreateLot = () => import('../views/CreateLot.vue');
const EditLot = () => import('../views/EditLot.vue');
const ViewSpot = () => import('../views/ViewSpot.vue');
const Users = () => import('../views/Users.vue');
const AdminSearch = () => import('../views/AdminSearch.vue');
const AdminSummary = () => import('../views/AdminSummary.vue');

const routes = [
  { 
    path: '/', 
    name: 'Home',
    redirect: () => {
      const token = localStorage.getItem('token');
      const role = localStorage.getItem('role');
      if (token && role) {
        return role === 'admin' ? '/admin/dashboard' : '/user/dashboard';
      }
      return '/login';
    }
  },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/user/dashboard', name: 'UserDashboard', component: UserDashboard },
  { path: '/user/book', name: 'BookSpot', component: BookSpot },
  { path: '/user/release/:reservationId', name: 'ReleaseSpot', component: ReleaseSpot, props: true },
  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/admin/lots/create', name: 'CreateLot', component: CreateLot },
  { path: '/admin/lots/:lotId/edit', name: 'EditLot', component: EditLot, props: true },
  { path: '/admin/spots/:spotId', name: 'ViewSpot', component: ViewSpot, props: true },
  { path: '/admin/users', name: 'Users', component: Users },
  { path: '/admin/search', name: 'AdminSearch', component: AdminSearch },
  { path: '/admin/summary', name: 'AdminSummary', component: AdminSummary },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const authRoutes = [
  'UserDashboard', 'BookSpot', 'ReleaseSpot',
  'AdminDashboard', 'CreateLot', 'EditLot', 'ViewSpot', 'Users', 'AdminSearch', 'AdminSummary'
];

const adminRoutes = [
  'AdminDashboard', 'CreateLot', 'EditLot', 'ViewSpot', 'Users', 'AdminSearch', 'AdminSummary'
];

const userRoutes = [
  'UserDashboard', 'BookSpot', 'ReleaseSpot'
];

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  if ((to.name === 'Login' || to.name === 'Signup') && token && role) {
    return next(role === 'admin' ? '/admin/dashboard' : '/user/dashboard');
  }
  
  if (authRoutes.includes(to.name)) {
    if (!token) {
      return next('/login');
    }
    
    if (adminRoutes.includes(to.name) && role !== 'admin') {
      return next('/user/dashboard');
    }
    
    if (userRoutes.includes(to.name) && role !== 'user') {
      return next('/admin/dashboard');
    }
  }
  
  next();
});

export default router; 