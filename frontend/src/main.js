import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import axios from 'axios';

axios.defaults.baseURL = 'http://192.168.215.2:5000';
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

createApp(App).use(router).mount('#app')
