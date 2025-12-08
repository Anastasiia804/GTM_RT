<template>
  <div class="health-status">
    <div class="status-grid">
      <div class="status-card active">
        <div class="status-icon">🟢</div>
        <div class="status-info">
          <div class="status-number">{{ health.active_containers }}</div>
          <div class="status-label">Active</div>
        </div>
      </div>

      <div class="status-card inactive">
        <div class="status-icon">🟡</div>
        <div class="status-info">
          <div class="status-number">{{ health.inactive_containers }}</div>
          <div class="status-label">Inactive</div>
        </div>
      </div>

      <div class="status-card never">
        <div class="status-icon">🔴</div>
        <div class="status-info">
          <div class="status-number">{{ health.never_loaded_containers }}</div>
          <div class="status-label">Never Loaded</div>
        </div>
      </div>

      <div class="status-card total">
        <div class="status-icon">📊</div>
        <div class="status-info">
          <div class="status-number">{{ health.total_containers }}</div>
          <div class="status-label">Total Containers</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HealthStatus',
  props: {
    health: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.status-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.status-icon {
  font-size: 36px;
}

.status-info {
  flex: 1;
}

.status-number {
  font-size: 32px;
  font-weight: bold;
  color: #2c3e50;
}

.status-label {
  font-size: 14px;
  color: #7f8c8d;
  margin-top: 5px;
}

.status-card.active {
  border-left: 4px solid #4CAF50;
}

.status-card.inactive {
  border-left: 4px solid #ff9800;
}

.status-card.never {
  border-left: 4px solid #f44336;
}

.status-card.total {
  border-left: 4px solid #2196F3;
}
</style>
