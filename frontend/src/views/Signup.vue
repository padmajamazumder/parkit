<template>
  <div class="signup-view">
    <h2>Signup</h2>
    <form @submit.prevent="handleSignup">
      <div>
        <label>Email:</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="password" type="password" required />
      </div>
      <div>
        <label>Full Name:</label>
        <input v-model="fullname" type="text" required />
      </div>
      <div>
        <label>Address:</label>
        <input v-model="address" type="text" required />
      </div>
      <div>
        <label>Pincode:</label>
        <input v-model="pincode" type="text" required />
      </div>
      <button type="submit">Sign Up</button>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </form>
    <router-link to="/login">Already have an account? Login</router-link>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const email = ref('');
const password = ref('');
const fullname = ref('');
const address = ref('');
const pincode = ref('');
const error = ref('');
const success = ref('');
const router = useRouter();

const handleSignup = async () => {
  error.value = '';
  success.value = '';
  try {
    await axios.post('/api/auth/signup', {
      email: email.value,
      password: password.value,
      fullname: fullname.value,
      address: address.value,
      pincode: pincode.value,
    });
    success.value = 'Signup successful! Redirecting to login...';
    setTimeout(() => router.push('/login'), 1500);
  } catch (err) {
    error.value = err.response?.data?.error || 'Signup failed';
  }
};
</script> 