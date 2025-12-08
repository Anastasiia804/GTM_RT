<template>
  <div class="advertiser-detail">
    <div v-if="loading">Loading...</div>
    <div v-else-if="!advertiser">Advertiser not found</div>
    <div v-else>
      <div class="page-header">
        <h2>{{ advertiser.name }}</h2>
        <router-link to="/advertisers" class="secondary" style="text-decoration: none; display: inline-block;">
          ← Back to Advertisers
        </router-link>
      </div>

      <!-- Advertiser Info -->
      <div class="card">
        <h3>Advertiser Information</h3>
        <div class="info-grid">
          <div class="info-item">
            <strong>Container ID:</strong>
            <code>{{ advertiser.container_id }}</code>
          </div>
          <div class="info-item">
            <strong>Status:</strong>
            <span :class="['status-badge', advertiser.is_active ? 'status-active' : 'status-inactive']">
              {{ advertiser.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <div class="info-item">
            <strong>Allowed Domains:</strong>
            <div v-if="advertiser.domains.length === 0">No domains configured</div>
            <ul v-else>
              <li v-for="domain in advertiser.domains" :key="domain">{{ domain }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Container Code -->
      <div class="card">
        <ContainerCode v-if="containerCode" :code="containerCode" />
      </div>

      <!-- Statistics -->
      <div class="card" v-if="stats">
        <h3>Container Statistics</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">Status</div>
            <div class="stat-value">
              <span :class="['status-badge', `status-${stats.status}`]">
                {{ stats.status === 'active' ? '🟢 Active' : stats.status === 'inactive' ? '🟡 Inactive' : '🔴 Never Loaded' }}
              </span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Loads Today</div>
            <div class="stat-value">{{ stats.loads_today }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Loads This Week</div>
            <div class="stat-value">{{ stats.loads_week }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Last Load</div>
            <div class="stat-value">{{ formatDate(stats.last_load) }}</div>
          </div>
        </div>
      </div>

      <!-- Scripts -->
      <div class="card">
        <div class="section-header">
          <h3>Container Scripts</h3>
          <button @click="showScriptForm = true" class="primary">+ Add Script</button>
        </div>

        <!-- Script Form -->
        <div v-if="showScriptForm" class="script-form-container">
          <ScriptEditor
            :script="editingScript || {}"
            @save="saveScript"
            @cancel="cancelScriptForm"
          />
        </div>

        <!-- Scripts List -->
        <div v-if="scripts.length === 0 && !showScriptForm" class="empty-state">
          <p>No scripts configured. Add a script to get started.</p>
        </div>
        <table v-else-if="scripts.length > 0">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="script in scripts" :key="script.id">
              <td>{{ script.name }}</td>
              <td>{{ script.script_type }}</td>
              <td>{{ script.priority }}</td>
              <td>
                <span :class="['status-badge', script.is_enabled ? 'status-active' : 'status-inactive']">
                  {{ script.is_enabled ? 'Enabled' : 'Disabled' }}
                </span>
              </td>
              <td class="actions-cell">
                <button @click="toggleScript(script)" class="secondary">
                  {{ script.is_enabled ? 'Disable' : 'Enable' }}
                </button>
                <button @click="editScript(script)" class="secondary">Edit</button>
                <button @click="deleteScript(script.id)" class="danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Logs -->
      <div class="card">
        <h3>Recent Activity Logs</h3>
        <div v-if="logs.length === 0">No activity yet</div>
        <table v-else>
          <thead>
            <tr>
              <th>Time</th>
              <th>Referer</th>
              <th>IP Address</th>
              <th>Allowed</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id">
              <td>{{ formatDate(log.created_at) }}</td>
              <td>{{ log.referer || 'N/A' }}</td>
              <td>{{ log.ip_address || 'N/A' }}</td>
              <td>
                <span :class="['status-badge', log.is_allowed ? 'status-active' : 'status-never']">
                  {{ log.is_allowed ? '✓' : '✗' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import ContainerCode from '../components/ContainerCode.vue'
import ScriptEditor from '../components/ScriptEditor.vue'

export default {
  name: 'AdvertiserDetail',
  components: {
    ContainerCode,
    ScriptEditor
  },
  setup() {
    const route = useRoute()
    const advertiserId = parseInt(route.params.id)
    
    const advertiser = ref(null)
    const containerCode = ref('')
    const stats = ref(null)
    const scripts = ref([])
    const logs = ref([])
    const loading = ref(false)
    const showScriptForm = ref(false)
    const editingScript = ref(null)

    const loadData = async () => {
      loading.value = true
      try {
        const [advRes, codeRes, statsRes, scriptsRes, logsRes] = await Promise.all([
          api.getAdvertiser(advertiserId),
          api.getAdvertiserCode(advertiserId),
          api.getAdvertiserStats(advertiserId),
          api.getAdvertiserScripts(advertiserId),
          api.getContainerLogs(advertiserId)
        ])
        
        advertiser.value = advRes.data
        containerCode.value = codeRes.data.code
        stats.value = statsRes.data
        scripts.value = scriptsRes.data
        logs.value = logsRes.data
      } catch (error) {
        console.error('Error loading advertiser details:', error)
      } finally {
        loading.value = false
      }
    }

    const saveScript = async (scriptData) => {
      try {
        if (editingScript.value) {
          await api.updateAdvertiserScript(advertiserId, editingScript.value.id, scriptData)
        } else {
          await api.createAdvertiserScript(advertiserId, scriptData)
        }
        await loadData()
        cancelScriptForm()
      } catch (error) {
        console.error('Error saving script:', error)
        alert('Error saving script')
      }
    }

    const editScript = (script) => {
      editingScript.value = { ...script }
      showScriptForm.value = true
    }

    const toggleScript = async (script) => {
      try {
        await api.toggleAdvertiserScript(advertiserId, script.id)
        await loadData()
      } catch (error) {
        console.error('Error toggling script:', error)
      }
    }

    const deleteScript = async (scriptId) => {
      if (!confirm('Are you sure you want to delete this script?')) return
      
      try {
        await api.deleteAdvertiserScript(advertiserId, scriptId)
        await loadData()
      } catch (error) {
        console.error('Error deleting script:', error)
      }
    }

    const cancelScriptForm = () => {
      showScriptForm.value = false
      editingScript.value = null
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return 'Never'
      const date = new Date(dateStr)
      return date.toLocaleString()
    }

    onMounted(() => {
      loadData()
    })

    return {
      advertiser,
      containerCode,
      stats,
      scripts,
      logs,
      loading,
      showScriptForm,
      editingScript,
      saveScript,
      editScript,
      toggleScript,
      deleteScript,
      cancelScriptForm,
      formatDate
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h2 {
  margin: 0;
  color: #2c3e50;
}

.info-grid {
  display: grid;
  gap: 15px;
}

.info-item strong {
  display: block;
  margin-bottom: 5px;
  color: #555;
}

.info-item code {
  background-color: #f5f5f5;
  padding: 4px 8px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.info-item ul {
  margin: 5px 0;
  padding-left: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
}

.stat-label {
  font-size: 14px;
  color: #777;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
}

.script-form-container {
  margin-bottom: 30px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

.actions-cell {
  display: flex;
  gap: 5px;
}

.actions-cell button {
  padding: 6px 12px;
  font-size: 12px;
}
</style>
