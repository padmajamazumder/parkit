<template>
  <div class="release-spot-view">
    <h2>Release Parking Spot</h2>
    <div v-if="reservation">
      <p><b>Reservation ID:</b> {{ reservation.reservation_id }}</p>
      <p><b>Lot ID:</b> {{ reservation.lot_id }}</p>
      <p><b>Spot ID:</b> {{ reservation.spot_id }}</p>
      <p><b>Vehicle Number:</b> {{ reservation.vehicle_number }}</p>
      <p><b>Parked In:</b> {{ formatDate(reservation.parking_timestamp) }}</p>
      <form @submit.prevent="handleRelease">
        <div class="button-group">
          <button type="submit" class="btn-danger">Release</button>
          <button type="button" class="btn-secondary" @click="goBack">Cancel</button>
        </div>
      </form>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>
    <div v-else>Loading reservation info...</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const reservationId = route.params.reservationId;
const reservation = ref(null);
const error = ref('');
const success = ref('');

const fetchReservation = async () => {
  try {
    const res = await axios.get('/api/user/dashboard');
    reservation.value = res.data.find(r => r.reservation_id == reservationId);
  } catch {
    reservation.value = null;
  }
};

const handleRelease = async () => {
  error.value = '';
  success.value = '';
  try {
    const res = await axios.post(`/api/user/release/${reservationId}`);
    success.value = `Spot released! Cost: ₹${res.data.cost}`;
    setTimeout(() => router.push('/user/dashboard'), 1500);
  } catch (err) {
    error.value = err.response?.data?.error || 'Release failed';
  }
};

const goBack = () => router.push('/user/dashboard');

const formatDate = (dt) => {
  if (!dt) return '-';
  return new Date(dt).toLocaleString();
};

onMounted(fetchReservation);
</script> 