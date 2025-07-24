<template>
  <div class="edit-lot-view">
    <h2>Edit Parking Lot</h2>
        <form v-if="loaded" @submit.prevent="handleUpdate">
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
        <button type="submit">Update</button>
        <button type="button" class="btn-secondary" @click="goBack">Cancel</button>
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </form>
    <div v-else class="loading">Loading lot info...</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const lotId = route.params.lotId;
const locationName = ref('');
const address = ref('');
const pincode = ref('');
const pricePerHour = ref(0);
const maxSpots = ref(1);
const error = ref('');
const success = ref('');
const loaded = ref(false);

const fetchLot = async () => {
  try {
    const res = await axios.get('/api/admin/lots');
    const lot = res.data.find(l => l.id == lotId);
    if (lot) {
      locationName.value = lot.location_name;
      address.value = lot.address;
      pincode.value = lot.pincode;
      pricePerHour.value = lot.price_per_hour;
      maxSpots.value = lot.max_spots;
      loaded.value = true;
    } else {
      error.value = 'Lot not found';
    }
  } catch {
    error.value = 'Failed to load lot info';
  }
};

const handleUpdate = async () => {
  error.value = '';
  success.value = '';
  try {
    await axios.put(`/api/admin/lots/${lotId}`, {
      location_name: locationName.value,
      address: address.value,
      pincode: pincode.value,
      price_per_hour: pricePerHour.value,
      max_spots: maxSpots.value,
    });
    success.value = 'Parking lot updated! Redirecting...';
    setTimeout(() => router.push('/admin/dashboard'), 1200);
  } catch (err) {
    error.value = err.response?.data?.error || 'Update failed';
  }
};

const goBack = () => router.push('/admin/dashboard');

onMounted(fetchLot);
</script> 