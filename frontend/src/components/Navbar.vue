<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h1>🏷️ TSPRTG Tag Manager</h1>
    </div>
    <div class="navbar-menu">
      <router-link to="/" class="nav-link">Dashboard</router-link>
      <router-link to="/advertisers" class="nav-link">Advertisers</router-link>
      <router-link to="/scripts" class="nav-link">Global Scripts</router-link>
      <router-link to="/health" class="nav-link">Health Monitor</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand h1 {
  font-size: 24px;
  font-weight: 600;
}

.navbar-menu {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #34495e;
}

.nav-link.router-link-active {
  background-color: #4CAF50;
}
</style>
