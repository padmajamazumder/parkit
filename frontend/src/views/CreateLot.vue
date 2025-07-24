<template>
  <div class="create-lot-view">
    <h2>Create Parking Lot</h2>
    <form @submit.prevent="handleCreate">
      <div>
        <label>Location Name:</label>
        <input v-model="locationName" type="text" required />
      </div>
      <div>
        <label>Address:</label>
        <input v-model="address" type="text" required />
      </div>
      <div>
        <label>PIN Code:</label>
        <input v-model="pincode" type="text" required />
      </div>
      <div>
        <label>Price (per hour):</label>
        <input v-model.number="pricePerHour" type="number" min="0" step="0.01" required />
      </div>
      <div>
        <label>Maximum Spots:</label>
        <input v-model.number="maxSpots" type="number" min="1" required />
      </div>
      <div class="button-group">
        <button type="submit">Add</button>
        <button type="button" class="btn-secondary" @click="goBack">Cancel</button>
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </form>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const locationName = ref('');
const address = ref('');
const pincode = ref('');
const pricePerHour = ref(0);
const maxSpots = ref(1);
const error = ref('');
const success = ref('');
const router = useRouter();

const handleCreate = async () => {
  error.value = '';
  success.value = '';
  try {
    await axios.post('/api/admin/lots', {
      location_name: locationName.value,
      address: address.value,
      pincode: pincode.value,
      price_per_hour: pricePerHour.value,
      max_spots: maxSpots.value,
    });
    success.value = 'Parking lot created! Redirecting...';
    setTimeout(() => router.push('/admin/dashboard'), 1200);
  } catch (err) {
    error.value = err.response?.data?.error || 'Creation failed';
  }
};

const goBack = () => router.push('/admin/dashboard');
</script> 