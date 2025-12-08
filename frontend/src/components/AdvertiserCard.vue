<template>
  <div class="advertiser-card" @click="$emit('click')">
    <div class="card-header">
      <h3>{{ advertiser.name }}</h3>
      <span :class="['status-badge', statusClass]">
        {{ statusText }}
      </span>
    </div>
    <div class="card-body">
      <div class="card-info">
        <strong>Container ID:</strong> <code>{{ advertiser.container_id }}</code>
      </div>
      <div class="card-info">
        <strong>Domains:</strong> {{ domainsText }}
      </div>
      <div class="card-info">
        <strong>Status:</strong> {{ advertiser.is_active ? 'Active' : 'Inactive' }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdvertiserCard',
  props: {
    advertiser: {
      type: Object,
      required: true
    },
    stats: {
      type: Object,
      default: null
    }
  },
  computed: {
    domainsText() {
      if (!this.advertiser.domains || this.advertiser.domains.length === 0) {
        return 'No domains configured'
      }
      return this.advertiser.domains.join(', ')
    },
    statusClass() {
      if (!this.stats) return 'status-badge'
      if (this.stats.status === 'active') return 'status-active'
      if (this.stats.status === 'inactive') return 'status-inactive'
      return 'status-never'
    },
    statusText() {
      if (!this.stats) return 'Unknown'
      if (this.stats.status === 'active') return '🟢 Active'
      if (this.stats.status === 'inactive') return '🟡 Inactive'
      return '🔴 Never Loaded'
    }
  }
}
</script>

<style scoped>
.advertiser-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.advertiser-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-info {
  font-size: 14px;
  color: #555;
}

.card-info code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}
</style>
