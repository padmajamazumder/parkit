<template>
  <div class="book-spot-view">
    <h2>Book Parking Spot</h2>
    <div v-if="lot">
      <p><b>Lot:</b> {{ lot.location_name }} (ID: {{ lot.id }})</p>
      <p><b>Address:</b> {{ lot.address }}</p>
      <p><b>Price per hour:</b> ₹{{ lot.price_per_hour }}</p>
      <form @submit.prevent="handleBook">
        <div>
          <label>Vehicle Number:</label>
          <input v-model="vehicleNumber" type="text" required placeholder="Enter your vehicle number" />
        </div>
        <div class="button-group">
          <button type="submit">Reserve</button>
          <button type="button" class="btn-secondary" @click="goBack">Cancel</button>
        </div>
      </form>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>
    <div v-else class="loading">Loading lot info...</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const lotId = route.query.lotId;
const lot = ref(null);
const vehicleNumber = ref('');
const error = ref('');
const success = ref('');

const fetchLot = async () => {
  try {
    const res = await axios.get('/api/user/search', { params: { location: '' } });
    lot.value = res.data.find(l => l.id == lotId);
  } catch {
    lot.value = null;
  }
};

const handleBook = async () => {
  error.value = '';
  success.value = '';
  try {
    await axios.post('/api/user/book', { lot_id: lotId, vehicle_number: vehicleNumber.value });
    success.value = 'Spot reserved! Redirecting...';
    setTimeout(() => router.push('/user/dashboard'), 1200);
  } catch (err) {
    error.value = err.response?.data?.error || 'Booking failed';
  }
};

const goBack = () => router.push('/user/dashboard');

onMounted(fetchLot);
</script> 