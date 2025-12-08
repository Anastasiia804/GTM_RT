<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
.main-content {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

:root {
  --primary-color: #4CAF50;
  --danger-color: #f44336;
  --warning-color: #ff9800;
  --info-color: #2196F3;
  --border-color: #ddd;
  --bg-light: #f5f5f5;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

button.primary {
  background-color: var(--primary-color);
  color: white;
}

button.primary:hover {
  background-color: #45a049;
}

button.danger {
  background-color: var(--danger-color);
  color: white;
}

button.danger:hover {
  background-color: #da190b;
}

button.secondary {
  background-color: var(--bg-light);
  color: #333;
  border: 1px solid var(--border-color);
}

button.secondary:hover {
  background-color: #e0e0e0;
}

input, textarea, select {
  padding: 8px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background-color: #4CAF50;
  color: white;
}

.status-inactive {
  background-color: #ff9800;
  color: white;
}

.status-never {
  background-color: #f44336;
  color: white;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th,
table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

table th {
  background-color: var(--bg-light);
  font-weight: 600;
}

table tr:hover {
  background-color: #f9f9f9;
}
</style>
