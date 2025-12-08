<template>
  <div class="health">
    <h2>Health Monitor</h2>

    <HealthStatus v-if="health" :health="health" />

    <div class="card">
      <h3>Containers Health Status</h3>
      
      <div v-if="loading">Loading...</div>
      <div v-else-if="containersHealth.length === 0">No containers found</div>
      <table v-else>
        <thead>
          <tr>
            <th>Advertiser</th>
            <th>Container ID</th>
            <th>Status</th>
            <th>Loads Today</th>
            <th>Loads Week</th>
            <th>Last Load</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="container in containersHealth" :key="container.container_id">
            <td>{{ container.advertiser_name }}</td>
            <td><code>{{ container.container_id }}</code></td>
            <td>
              <span :class="['status-badge', `status-${container.status}`]">
                {{ getStatusText(container.status) }}
              </span>
            </td>
            <td>{{ container.loads_today }}</td>
            <td>{{ container.loads_week }}</td>
            <td>{{ formatDate(container.last_load) }}</td>
            <td>
              <button @click="viewLogs(container.advertiser_id)" class="secondary">View Logs</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Logs Modal -->
    <div v-if="showLogsModal" class="modal-overlay" @click="closeLogsModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Activity Logs</h3>
          <button @click="closeLogsModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="loadingLogs">Loading logs...</div>
          <div v-else-if="logs.length === 0">No logs found</div>
          <table v-else>
            <thead>
              <tr>
                <th>Time</th>
                <th>Referer</th>
                <th>IP Address</th>
                <th>User Agent</th>
                <th>Allowed</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in logs" :key="log.id">
                <td>{{ formatDate(log.created_at) }}</td>
                <td class="truncate">{{ log.referer || 'N/A' }}</td>
                <td>{{ log.ip_address || 'N/A' }}</td>
                <td class="truncate">{{ truncate(log.user_agent, 50) || 'N/A' }}</td>
                <td>
                  <span :class="['status-badge', log.is_allowed ? 'status-active' : 'status-never']">
                    {{ log.is_allowed ? '✓ Allowed' : '✗ Blocked' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../api'
import HealthStatus from '../components/HealthStatus.vue'

export default {
  name: 'Health',
  components: {
    HealthStatus
  },
  setup() {
    const health = ref(null)
    const containersHealth = ref([])
    const loading = ref(false)
    const showLogsModal = ref(false)
    const loadingLogs = ref(false)
    const logs = ref([])
    const currentAdvertiserId = ref(null)

    const loadData = async () => {
      loading.value = true
      try {
        const [healthRes, containersRes] = await Promise.all([
          api.getHealth(),
          api.getContainersHealth()
        ])
        health.value = healthRes.data
        containersHealth.value = containersRes.data
      } catch (error) {
        console.error('Error loading health data:', error)
      } finally {
        loading.value = false
      }
    }

    const viewLogs = async (advertiserId) => {
      currentAdvertiserId.value = advertiserId
      showLogsModal.value = true
      loadingLogs.value = true
      
      try {
        const response = await api.getContainerLogs(advertiserId)
        logs.value = response.data
      } catch (error) {
        console.error('Error loading logs:', error)
      } finally {
        loadingLogs.value = false
      }
    }

    const closeLogsModal = () => {
      showLogsModal.value = false
      logs.value = []
      currentAdvertiserId.value = null
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return 'Never'
      const date = new Date(dateStr)
      return date.toLocaleString()
    }

    const getStatusText = (status) => {
      if (status === 'active') return '🟢 Active'
      if (status === 'inactive') return '🟡 Inactive'
      return '🔴 Never Loaded'
    }

    const truncate = (text, length) => {
      if (!text) return ''
      if (text.length <= length) return text
      return text.substring(0, length) + '...'
    }

    onMounted(() => {
      loadData()
      // Auto-refresh every 30 seconds
      const interval = setInterval(loadData, 30000)
      return () => clearInterval(interval)
    })

    return {
      health,
      containersHealth,
      loading,
      showLogsModal,
      loadingLogs,
      logs,
      viewLogs,
      closeLogsModal,
      formatDate,
      getStatusText,
      truncate
    }
  }
}
</script>

<style scoped>
h2 {
  margin-bottom: 30px;
  color: #2c3e50;
}

.truncate {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1200px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 32px;
  height: 32px;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.modal-body table {
  font-size: 13px;
}
</style>
