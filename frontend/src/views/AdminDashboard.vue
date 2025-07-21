<template>
  <div class="admin-dashboard-view">
    <div class="dashboard-header">
      <h2>Admin Dashboard</h2>
      <button @click="refreshData" class="refresh-btn" :disabled="loading">
        <span v-if="loading">🔄</span>
        <span v-else>🔄</span>
        {{ loading ? 'Refreshing...' : 'Refresh Data' }}
      </button>
    </div>
    <nav class="admin-nav">
      <router-link to="/admin/dashboard">Home</router-link>
      <router-link to="/admin/users">Users</router-link>
      <router-link to="/admin/search">Search</router-link>
      <router-link to="/admin/summary">Summary</router-link>
      <button @click="createLot">Create Parking Lot</button>
    </nav>
    <div class="lots-container">
      <div v-for="lot in lots" :key="lot.id" class="lot-box" @click="editLot(lot.id)">
        <h3>{{ lot.location_name }}</h3>
        <p>{{ lot.address }} ({{ lot.pincode }})</p>
        <p>Price/hr: ₹{{ lot.price_per_hour }}</p>
        <div class="spots-container">
          <div
            v-for="spot in lot.spots"
            :key="spot.id"
            class="spot-box"
            :class="{ occupied: spot.status === 'O', available: spot.status === 'A' }"
            @click.stop="viewSpot(spot.id)"
          >
            {{ spot.id }}
          </div>
        </div>
      </div>
    </div>
    <div v-if="!lots.length" class="text-center mt-2">No parking lots found.</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const lots = ref([]);
const loading = ref(false);
const router = useRouter();

const fetchLots = async () => {
  loading.value = true;
  try {
    const res = await axios.get('/api/admin/lots');
    lots.value = await Promise.all(res.data.map(async lot => {
      const spotsRes = await axios.get(`/api/admin/search`, { params: { location: lot.location_name } });
      const lotWithSpots = spotsRes.data.find(l => l.id === lot.id);
      return { ...lot, spots: lotWithSpots ? lotWithSpots.spots : [] };
    }));
  } catch {
    lots.value = [];
  } finally {
    loading.value = false;
  }
};

const refreshData = () => {
  fetchLots();
};

const createLot = () => router.push('/admin/lots/create');
const editLot = (lotId) => router.push(`/admin/lots/${lotId}/edit`);
const viewSpot = (spotId) => router.push(`/admin/spots/${spotId}`);

onMounted(fetchLots);
</script>
<style>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.dashboard-header h2 {
  margin: 0;
  color: var(--color-heading);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  color: var(--color-text);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: var(--color-background-mute);
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-btn span {
  display: inline-block;
  transition: transform 0.5s;
}

.refresh-btn:disabled span {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

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
  cursor: pointer;
  background: var(--color-background-soft);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s, transform 0.2s;
}

.lot-box:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.lot-box h3 {
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
  background: var(--color-background);
  border: 1px solid var(--color-border);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
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

.spot-box:hover {
  opacity: 0.8;
}
</style> 