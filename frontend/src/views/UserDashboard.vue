<template>
  <div class="user-dashboard-view">
    <h2>User Dashboard</h2>
    <section>
      <h3>Parking History</h3>
      <table v-if="history.length">
        <thead>
          <tr>
            <th>Reservation ID</th>
            <th>Lot ID</th>
            <th>Spot ID</th>
            <th>Vehicle</th>
            <th>Parked In</th>
            <th>Parked Out</th>
            <th>Cost</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in history" :key="r.reservation_id">
            <td>{{ r.reservation_id }}</td>
            <td>{{ r.lot_id }}</td>
            <td>{{ r.spot_id }}</td>
            <td>{{ r.vehicle_number }}</td>
            <td>{{ formatDate(r.parking_timestamp) }}</td>
            <td>{{ r.leaving_timestamp ? formatDate(r.leaving_timestamp) : '-' }}</td>
            <td>{{ r.parking_cost ? `₹${r.parking_cost}` : '-' }}</td>
            <td :class="r.status === 'Active' ? 'status-active' : 'status-completed'">{{ r.status }}</td>
            <td>
              <button v-if="r.status === 'Active'" @click="release(r.reservation_id)">Release</button>
              <span v-else>Parked Out</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-message">No parking history found.</div>
    </section>
    <section class="dashboard-section">
      <h3>Search Parking Lots</h3>
      <form @submit.prevent="searchLots" class="search-form">
        <input v-model="searchLocation" type="search" placeholder="Enter location..." />
        <button type="submit">Search</button>
      </form>
      <div v-if="lots.length">
        <table>
          <thead>
            <tr>
              <th>Lot</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Price/hr</th>
              <th>Available Spots</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in lots" :key="lot.id">
              <td>{{ lot.location_name }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.pincode }}</td>
              <td>₹{{ lot.price_per_hour }}</td>
              <td>{{ lot.available_spots }}</td>
              <td>
                <button :disabled="lot.available_spots === 0" @click="book(lot)">Book</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="searched" class="empty-message">No lots found.</div>
    </section>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const history = ref([]);
const lots = ref([]);
const searchLocation = ref('');
const searched = ref(false);
const router = useRouter();

const fetchHistory = async () => {
  try {
    const res = await axios.get('/api/user/dashboard');
    history.value = res.data;
  } catch (err) {
    history.value = [];
  }
};

const searchLots = async () => {
  try {
    const res = await axios.get('/api/user/search', {
      params: { location: searchLocation.value }
    });
    lots.value = res.data;
    searched.value = true;
  } catch (err) {
    lots.value = [];
    searched.value = true;
  }
};

const book = (lot) => {
  router.push({ name: 'BookSpot', query: { lotId: lot.id } });
};

const release = (reservationId) => {
  router.push({ name: 'ReleaseSpot', params: { reservationId } });
};

const formatDate = (dt) => {
  if (!dt) return '-';
  return new Date(dt).toLocaleString();
};

onMounted(() => {
  fetchHistory();
});
</script>
<style>
button {
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

table {
  color: var(--color-text);
}

table th {
  color: var(--color-heading);
}

table td {
  color: var(--color-text);
}

/* Better styling for empty states */
.empty-message {
  color: var(--color-text);
  text-align: center;
  padding: 2rem;
  background: var(--color-background-soft);
  border-radius: 8px;
  border: 1px solid var(--color-border);
  margin: 1rem 0;
}
</style> 