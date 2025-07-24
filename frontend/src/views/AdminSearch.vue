<template>
  <div class="admin-search-view">
    <h2>Admin Search</h2>
    <nav class="admin-nav">
      <router-link to="/admin/dashboard">Home</router-link>
      <router-link to="/admin/users">Users</router-link>
      <router-link to="/admin/search">Search</router-link>
      <router-link to="/admin/summary">Summary</router-link>
    </nav>
    
    <form @submit.prevent="searchLots" class="search-form">
      <div>
        <label>Search by Location:</label>
        <input v-model="location" placeholder="Enter location name..." />
      </div>
      <div>
        <label>Search by User ID:</label>
        <input v-model="userId" placeholder="Enter user ID..." />
      </div>
      <button type="submit">Search</button>
    </form>
    
    <div v-if="lots.length" class="search-results">
      <h3>Search Results</h3>
      <div class="lots-container">
        <div v-for="lot in lots" :key="lot.id" class="lot-box">
          <h4>{{ lot.location_name }}</h4>
          <p>{{ lot.address }} ({{ lot.pincode }})</p>
          <p>Price/hr: ₹{{ lot.price_per_hour }}</p>
          <div class="spots-container">
            <div
              v-for="spot in lot.spots"
              :key="spot.id"
              class="spot-box"
              :class="{ 
                occupied: spot.status === 'O', 
                available: spot.status === 'A',
                'reserved-by-user': spot.reserved_by_user
              }"
              @click="viewSpot(spot.id)"
            >
              {{ spot.id }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="searched" class="no-results">
      No parking lots found matching your search criteria.
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const location = ref('');
const userId = ref('');
const lots = ref([]);
const searched = ref(false);
const router = useRouter();

const searchLots = async () => {
  if (!location.value && !userId.value) {
    alert('Please enter either a location or user ID to search.');
    return;
  }
  
  try {
    const params = {};
    if (location.value) params.location = location.value;
    if (userId.value) params.user_id = userId.value;
    
    const res = await axios.get('/api/admin/search', { params });
    lots.value = res.data;
    searched.value = true;
  } catch (err) {
    console.error('Search failed:', err);
    lots.value = [];
    searched.value = true;
  }
};

const viewSpot = (spotId) => router.push(`/admin/spots/${spotId}`);
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

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: end;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--color-background-soft);
  border-radius: 8px;
  border: 1px solid var(--color-border);
  box-sizing: border-box;
}

.search-form div {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 200px;
}

.search-form label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-heading);
}

.search-form input {
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
  background: var(--color-background);
  color: var(--color-text);
}

.search-form input:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 0 2px hsla(160, 100%, 37%, 0.2);
}

.search-form button {
  padding: 0.75rem 1.5rem;
  background: hsla(160, 100%, 37%, 1);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
  height: fit-content;
  align-self: flex-end;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.search-form button:hover {
  background: hsla(160, 100%, 32%, 1);
}

.lots-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.lot-box {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
  min-width: 250px;
  background: var(--color-background-soft);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s, transform 0.2s;
}

.lot-box:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.lot-box h4 {
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.lot-box p {
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.spots-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.spot-box {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  border: 1px solid var(--color-border);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
  background: var(--color-background);
  transition: background-color 0.2s;
}

.spot-box.occupied {
  background: #ffebee;
  color: #c62828;
  border-color: #e57373;
}

.spot-box.available {
  background: #e8f5e8;
  color: #2e7d32;
  border-color: #81c784;
}

.spot-box.reserved-by-user {
  background: #fff3e0;
  color: #f57c00;
  border: 2px solid #ff9800;
  font-weight: bold;
}

.no-results {
  text-align: center;
  color: var(--color-text);
  margin-top: 2rem;
  padding: 2rem;
  background: var(--color-background-soft);
  border-radius: 8px;
  border: 1px solid var(--color-border);
}
</style> 