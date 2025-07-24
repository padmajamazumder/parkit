<template>
  <div class="users-view">
    <h2>Users List</h2>
    <nav class="admin-nav">
      <router-link to="/admin/dashboard">Home</router-link>
      <router-link to="/admin/users">Users</router-link>
      <router-link to="/admin/search">Search</router-link>
      <router-link to="/admin/summary">Summary</router-link>
    </nav>
    
    <div class="search-section">
      <input v-model="searchTerm" type="search" placeholder="Search by name or email..." @input="filterUsers" />
      <span>Total Users: {{ filteredUsers.length }}</span>
    </div>
    
    <table v-if="filteredUsers.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Full Name</th>
          <th>Address</th>
          <th>Pincode</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filteredUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.fullname }}</td>
          <td>{{ user.address }}</td>
          <td>{{ user.pincode }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else-if="users.length">No users match your search.</div>
    <div v-else>No users found.</div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const users = ref([]);
const searchTerm = ref('');

const filteredUsers = computed(() => {
  if (!searchTerm.value) return users.value;
  const term = searchTerm.value.toLowerCase();
  return users.value.filter(user => 
    user.fullname.toLowerCase().includes(term) ||
    user.email.toLowerCase().includes(term)
  );
});

const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/admin/users');
    users.value = res.data;
  } catch (err) {
    console.error('Failed to fetch users:', err);
    users.value = [];
  }
};

onMounted(fetchUsers);
</script>
<style>
.admin-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.admin-nav a {
  color: var(--color-text);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.admin-nav a:hover,
.admin-nav a.router-link-active {
  background-color: var(--color-background-mute);
}

.search-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.search-section input {
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  width: 300px;
  background: var(--color-background);
  color: var(--color-text);
}

.search-section input:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 0 2px hsla(160, 100%, 37%, 0.2);
}
</style> 