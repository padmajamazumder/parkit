<template>
  <div class="admin-summary-view">
    <h2>Admin Summary</h2>
    <nav class="admin-nav">
      <router-link to="/admin/dashboard">Home</router-link>
      <router-link to="/admin/users">Users</router-link>
      <router-link to="/admin/search">Search</router-link>
      <router-link to="/admin/summary">Summary</router-link>
    </nav>
    <div v-if="summary.length">
      <table>
        <thead>
          <tr>
            <th>Lot Name</th>
            <th>Revenue (₹)</th>
            <th>Available Spots</th>
            <th>Occupied Spots</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in summary" :key="lot.id">
            <td>{{ lot.location_name }}</td>
            <td>{{ lot.revenue }}</td>
            <td>{{ lot.available_spots }}</td>
            <td>{{ lot.occupied_spots }}</td>
          </tr>
        </tbody>
      </table>
      <div class="mt-2">
        <canvas id="revenueChart" height="120"></canvas>
      </div>
    </div>
    <div v-else class="empty-state">No summary data available.</div>
  </div>
</template>
<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
let Chart;

const summary = ref([]);

const fetchSummary = async () => {
  try {
    const res = await axios.get('/api/admin/summary');
    summary.value = res.data;
    await nextTick();
    renderChart();
  } catch (err) {
    summary.value = [];
  }
};

const renderChart = async () => {
  if (!summary.value.length) return;
  if (!Chart) {
    Chart = (await import('chart.js/auto')).default;
  }
  const ctx = document.getElementById('revenueChart');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: summary.value.map(lot => lot.location_name),
      datasets: [
        {
          label: 'Revenue (₹)',
          data: summary.value.map(lot => lot.revenue),
          backgroundColor: '#007bff',
        },
        {
          label: 'Available Spots',
          data: summary.value.map(lot => lot.available_spots),
          backgroundColor: '#28a745',
        },
        {
          label: 'Occupied Spots',
          data: summary.value.map(lot => lot.occupied_spots),
          backgroundColor: '#dc3545',
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Parking Lot Revenue & Spot Status' },
      },
    },
  });
};

onMounted(fetchSummary);
</script>
<style>
.admin-nav {
  display: flex;
  gap: 1em;
  margin-bottom: 1.5em;
  align-items: center;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 2em;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
th {
  background: #f0f0f0;
}
</style> 