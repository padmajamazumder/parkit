<template>
  <div class="view-spot-view">
    <div class="spot-header">
      <h2>🅿️ Parking Spot Details</h2>
      <button @click="goBack" class="btn-back">← Back to Dashboard</button>
    </div>
    
    <div v-if="spot" class="spot-content">
      <div class="spot-status-card" :class="spotStatusClass">
        <div class="status-icon">
          {{ spot.status === 'O' ? '🚗' : '🅿️' }}
        </div>
        <div class="status-info">
          <h3>Spot #{{ spot.id }}</h3>
          <span class="status-badge" :class="spot.status === 'O' ? 'occupied' : 'available'">
            {{ spot.status === 'O' ? 'Occupied' : 'Available' }}
          </span>
        </div>
      </div>

      <div class="info-card">
        <h4>📍 Location Information</h4>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Spot ID:</span>
            <span class="value">#{{ spot.id }}</span>
          </div>
          <div class="info-item">
            <span class="label">Parking Lot:</span>
            <span class="value">Lot #{{ spot.lot_id }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="spot.status === 'O' && reservation" class="info-card occupied-details">
        <h4>🚗 Current Reservation</h4>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Customer ID:</span>
            <span class="value">#{{ reservation.user_id }}</span>
          </div>
          <div class="info-item">
            <span class="label">Vehicle Number:</span>
            <span class="value vehicle-number">{{ reservation.vehicle_number }}</span>
          </div>
          <div class="info-item">
            <span class="label">Parked Since:</span>
            <span class="value">{{ formatDate(reservation.parking_timestamp) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Current Cost:</span>
            <span class="value cost">{{ reservation.parking_cost ? `₹${reservation.parking_cost}` : 'Calculating...' }}</span>
          </div>
        </div>
        <div class="duration-info">
          <span class="duration-label">⏱️ Duration:</span>
          <span class="duration-value">{{ calculateDuration(reservation.parking_timestamp) }}</span>
        </div>
      </div>
      
      <div v-else-if="spot.status === 'A'" class="info-card available-actions">
        <h4>✅ Available for Booking</h4>
        <p class="available-message">This parking spot is currently available and ready for new reservations.</p>
        <div class="action-section">
          <button @click="deleteSpot" class="btn-danger">
            🗑️ Delete Spot
          </button>
        </div>
      </div>

      <div v-if="error" class="message error">
        ⚠️ {{ error }}
      </div>
      <div v-if="success" class="message success">
        ✅ {{ success }}
      </div>
    </div>
    
    <div v-else class="loading-state">
      <div class="loading-spinner">🔄</div>
      <p>Loading spot information...</p>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const spotId = route.params.spotId;
const spot = ref(null);
const reservation = ref(null);
const error = ref('');
const success = ref('');

const spotStatusClass = computed(() => {
  if (!spot.value) return '';
  return spot.value.status === 'O' ? 'occupied-card' : 'available-card';
});

const fetchSpot = async () => {
  try {
    const res = await axios.get(`/api/admin/spots/${spotId}`);
    spot.value = res.data;
    
    // If spot is occupied, fetch reservation details
    if (spot.value.status === 'O') {
      try {
        const reservationRes = await axios.get(`/api/admin/spots/${spotId}/reservation`);
        reservation.value = reservationRes.data;
      } catch (err) {
        // Handle case where reservation details can't be fetched
        console.error('Failed to fetch reservation details:', err);
      }
    }
  } catch {
    error.value = 'Failed to load spot info';
  }
};

// Auto-refresh cost every 30 seconds for occupied spots
let refreshInterval = null;

const startCostRefresh = () => {
  if (refreshInterval) clearInterval(refreshInterval);
  
  refreshInterval = setInterval(async () => {
    if (spot.value?.status === 'O') {
      try {
        const reservationRes = await axios.get(`/api/admin/spots/${spotId}/reservation`);
        reservation.value = reservationRes.data;
      } catch (err) {
        console.error('Failed to refresh reservation details:', err);
      }
    } else {
      clearInterval(refreshInterval);
    }
  }, 30000); // Refresh every 30 seconds
};

const stopCostRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
    refreshInterval = null;
  }
};

const deleteSpot = async () => {
  if (!confirm('Are you sure you want to delete this spot?')) return;
  
  error.value = '';
  success.value = '';
  try {
    await axios.delete(`/api/admin/spots/${spotId}`);
    success.value = 'Spot deleted! Redirecting...';
    setTimeout(() => router.push('/admin/dashboard'), 1200);
  } catch (err) {
    error.value = err.response?.data?.error || 'Delete failed';
  }
};

const goBack = () => router.push('/admin/dashboard');

const formatDate = (dt) => {
  if (!dt) return '-';
  return new Date(dt).toLocaleString();
};

const calculateDuration = (timestamp) => {
  if (!timestamp) return '-';
  
  const start = new Date(timestamp);
  const now = new Date();
  const diffMs = now - start;
  
  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else {
    return `${minutes}m`;
  }
};

onMounted(async () => {
  await fetchSpot();
  if (spot.value?.status === 'O') {
    startCostRefresh();
  }
});

onUnmounted(() => {
  stopCostRefresh();
});
</script>

<style scoped>
.view-spot-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.spot-header {
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-border);
}

.spot-header h2 {
  margin: 0;
  color: var(--color-heading);
  font-size: 1.8rem;
}

.btn-back {
  background: var(--color-background-mute) !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-border) !important;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-back:hover {
  background: var(--color-background-soft) !important;
  transform: translateX(-2px);
}

.spot-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.spot-status-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border: 2px solid;
  transition: transform 0.2s;
}

.spot-status-card:hover {
  transform: translateY(-2px);
}

.occupied-card {
  background: linear-gradient(135deg, #ffebee, #ffcdd2);
  border-color: #e57373;
}

.available-card {
  background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
  border-color: #81c784;
}

.status-icon {
  font-size: 3rem;
  line-height: 1;
}

.status-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: var(--color-heading);
}

.status-badge {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.occupied {
  background: #c62828;
  color: white;
}

.status-badge.available {
  background: #2e7d32;
  color: white;
}

.info-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.info-card h4 {
  margin: 0 0 1rem 0;
  color: var(--color-heading);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--color-background);
  border-radius: 6px;
  border: 1px solid var(--color-border);
}

.label {
  font-weight: 600;
  color: var(--color-text);
}

.value {
  font-weight: 500;
  color: var(--color-heading);
}

.vehicle-number {
  font-family: 'Courier New', monospace;
  background: var(--color-background-mute);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
}

.cost {
  color: #2e7d32;
  font-weight: 700;
  font-size: 1.1rem;
}

.duration-info {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--color-background);
  border-radius: 8px;
  border-left: 4px solid #ff9800;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.duration-label {
  font-weight: 600;
  color: var(--color-text);
}

.duration-value {
  font-weight: 700;
  font-size: 1.2rem;
  color: #ff9800;
}

.occupied-details {
  border-left: 4px solid #c62828;
}

.available-actions {
  border-left: 4px solid #2e7d32;
  text-align: center;
}

.available-message {
  color: var(--color-text);
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.action-section {
  margin-top: 1rem;
}

.btn-danger {
  background: #d32f2f !important;
  color: white !important;
  border: none !important;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-danger:hover {
  background: #c62828 !important;
  transform: translateY(-1px);
}

.message {
  padding: 1rem;
  border-radius: 6px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.message.error {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #e57373;
}

.message.success {
  background: #e8f5e8;
  color: #2e7d32;
  border: 1px solid #81c784;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--color-text);
}

.loading-spinner {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive design */
@media (max-width: 768px) {
  .spot-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .spot-status-card {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .info-item {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .duration-info {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .occupied-card {
    background: linear-gradient(135deg, #4a2c2a, #5d2f2f);
  }
  
  .available-card {
    background: linear-gradient(135deg, #2e4e2e, #3e5e3e);
  }
}
</style> 