<template>
  <div class="advertisers">
    <div class="page-header">
      <h2>Advertisers</h2>
      <button @click="showCreateForm = true" class="primary">+ Create Advertiser</button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="showCreateForm" class="card">
      <h3>{{ editingAdvertiser ? 'Edit' : 'Create' }} Advertiser</h3>
      <div class="form-group">
        <label>Name</label>
        <input v-model="formData.name" type="text" placeholder="Enter advertiser name" />
      </div>

      <div class="form-group">
        <label>Allowed Domains (one per line)</label>
        <textarea
          v-model="domainsText"
          rows="4"
          placeholder="example.com&#10;subdomain.example.com"
        ></textarea>
      </div>

      <div class="form-group">
        <label>
          <input v-model="formData.is_active" type="checkbox" />
          Active
        </label>
      </div>

      <div class="form-actions">
        <button @click="saveAdvertiser" class="primary">Save</button>
        <button @click="cancelForm" class="secondary">Cancel</button>
      </div>
    </div>

    <!-- Advertisers List -->
    <div v-if="loading">Loading...</div>
    <div v-else-if="advertisers.length === 0" class="card">
      <p>No advertisers yet. Create one to get started!</p>
    </div>
    <div v-else class="advertisers-grid">
      <div v-for="advertiser in advertisers" :key="advertiser.id" class="advertiser-item card">
        <AdvertiserCard
          :advertiser="advertiser"
          :stats="getStats(advertiser.container_id)"
          @click="goToAdvertiser(advertiser.id)"
        />
        <div class="card-actions">
          <button @click.stop="editAdvertiser(advertiser)" class="secondary">Edit</button>
          <button @click.stop="deleteAdvertiser(advertiser.id)" class="danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import AdvertiserCard from '../components/AdvertiserCard.vue'

export default {
  name: 'Advertisers',
  components: {
    AdvertiserCard
  },
  setup() {
    const router = useRouter()
    const advertisers = ref([])
    const containersHealth = ref([])
    const loading = ref(false)
    const showCreateForm = ref(false)
    const editingAdvertiser = ref(null)
    const formData = ref({
      name: '',
      domains: [],
      is_active: true
    })

    const domainsText = computed({
      get: () => formData.value.domains.join('\n'),
      set: (value) => {
        formData.value.domains = value.split('\n').map(d => d.trim()).filter(d => d)
      }
    })

    const loadData = async () => {
      loading.value = true
      try {
        const [advertisersRes, containersRes] = await Promise.all([
          api.getAdvertisers(),
          api.getContainersHealth()
        ])
        advertisers.value = advertisersRes.data
        containersHealth.value = containersRes.data
      } catch (error) {
        console.error('Error loading advertisers:', error)
      } finally {
        loading.value = false
      }
    }

    const getStats = (containerId) => {
      return containersHealth.value.find(c => c.container_id === containerId) || null
    }

    const saveAdvertiser = async () => {
      try {
        if (editingAdvertiser.value) {
          await api.updateAdvertiser(editingAdvertiser.value.id, formData.value)
        } else {
          await api.createAdvertiser(formData.value)
        }
        await loadData()
        cancelForm()
      } catch (error) {
        console.error('Error saving advertiser:', error)
        alert('Error saving advertiser')
      }
    }

    const editAdvertiser = (advertiser) => {
      editingAdvertiser.value = advertiser
      formData.value = {
        name: advertiser.name,
        domains: [...advertiser.domains],
        is_active: advertiser.is_active
      }
      showCreateForm.value = true
    }

    const deleteAdvertiser = async (id) => {
      if (!confirm('Are you sure you want to delete this advertiser?')) return
      
      try {
        await api.deleteAdvertiser(id)
        await loadData()
      } catch (error) {
        console.error('Error deleting advertiser:', error)
        alert('Error deleting advertiser')
      }
    }

    const cancelForm = () => {
      showCreateForm.value = false
      editingAdvertiser.value = null
      formData.value = {
        name: '',
        domains: [],
        is_active: true
      }
    }

    const goToAdvertiser = (id) => {
      router.push(`/advertisers/${id}`)
    }

    onMounted(() => {
      loadData()
    })

    return {
      advertisers,
      loading,
      showCreateForm,
      editingAdvertiser,
      formData,
      domainsText,
      getStats,
      saveAdvertiser,
      editAdvertiser,
      deleteAdvertiser,
      cancelForm,
      goToAdvertiser
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

.advertisers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.advertiser-item {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.card-actions {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
</style>
