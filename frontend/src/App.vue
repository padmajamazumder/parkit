<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const fullname = ref(localStorage.getItem('fullname') || '');
const isAuthenticated = computed(() => !!localStorage.getItem('token'));

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  localStorage.removeItem('fullname');
  router.push('/login');
};
</script>

<template>
  <div id="app">
    <nav v-if="isAuthenticated">
      <span>Welcome, {{ fullname }}</span>
      <button @click="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<style>
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav span {
  color: var(--color-heading);
  font-weight: 600;
}
</style>
