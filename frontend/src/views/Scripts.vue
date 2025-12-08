<template>
  <div class="scripts">
    <div class="page-header">
      <h2>Global Scripts</h2>
      <button @click="showScriptForm = true" class="primary">+ Add Global Script</button>
    </div>

    <div class="card">
      <p class="info-text">
        Global scripts are loaded for all advertisers. They execute before advertiser-specific scripts.
      </p>

      <!-- Script Form -->
      <div v-if="showScriptForm" class="script-form-container">
        <ScriptEditor
          :script="editingScript || {}"
          @save="saveScript"
          @cancel="cancelScriptForm"
        />
      </div>

      <!-- Scripts List -->
      <div v-if="loading">Loading...</div>
      <div v-else-if="scripts.length === 0 && !showScriptForm" class="empty-state">
        <p>No global scripts configured.</p>
      </div>
      <table v-else-if="scripts.length > 0">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Content</th>
            <th>Priority</th>
            <th>Async</th>
            <th>Defer</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="script in scripts" :key="script.id">
            <td>{{ script.name }}</td>
            <td>{{ script.script_type }}</td>
            <td class="content-cell">
              <code>{{ truncate(script.content, 50) }}</code>
            </td>
            <td>{{ script.priority }}</td>
            <td>{{ script.is_async ? '✓' : '✗' }}</td>
            <td>{{ script.is_defer ? '✓' : '✗' }}</td>
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../api'
import ScriptEditor from '../components/ScriptEditor.vue'

export default {
  name: 'Scripts',
  components: {
    ScriptEditor
  },
  setup() {
    const scripts = ref([])
    const loading = ref(false)
    const showScriptForm = ref(false)
    const editingScript = ref(null)

    const loadScripts = async () => {
      loading.value = true
      try {
        const response = await api.getScripts()
        scripts.value = response.data
      } catch (error) {
        console.error('Error loading scripts:', error)
      } finally {
        loading.value = false
      }
    }

    const saveScript = async (scriptData) => {
      try {
        if (editingScript.value) {
          await api.updateScript(editingScript.value.id, scriptData)
        } else {
          await api.createScript(scriptData)
        }
        await loadScripts()
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
        await api.toggleScript(script.id)
        await loadScripts()
      } catch (error) {
        console.error('Error toggling script:', error)
      }
    }

    const deleteScript = async (scriptId) => {
      if (!confirm('Are you sure you want to delete this script?')) return
      
      try {
        await api.deleteScript(scriptId)
        await loadScripts()
      } catch (error) {
        console.error('Error deleting script:', error)
      }
    }

    const cancelScriptForm = () => {
      showScriptForm.value = false
      editingScript.value = null
    }

    const truncate = (text, length) => {
      if (text.length <= length) return text
      return text.substring(0, length) + '...'
    }

    onMounted(() => {
      loadScripts()
    })

    return {
      scripts,
      loading,
      showScriptForm,
      editingScript,
      saveScript,
      editScript,
      toggleScript,
      deleteScript,
      cancelScriptForm,
      truncate
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

.info-text {
  background-color: #e3f2fd;
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #2196F3;
  margin-bottom: 20px;
}

.script-form-container {
  margin-bottom: 30px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

.content-cell code {
  font-size: 12px;
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
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
