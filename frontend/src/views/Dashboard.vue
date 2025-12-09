<template>
  <div class="dashboard">
    <h2>Dashboard</h2>
    
    <HealthStatus v-if="health" :health="health" />

    <div class="card" style="margin-top: 30px;">
      <h3>Recent Advertisers</h3>
      <div v-if="loading">Loading...</div>
      <div v-else-if="advertisers.length === 0">
        <p>No advertisers yet. <router-link to="/advertisers">Create one</router-link></p>
      </div>
      <div v-else class="advertisers-grid">
        <AdvertiserCard
          v-for="advertiser in advertisers.slice(0, 6)"
          :key="advertiser.id"
          :advertiser="advertiser"
          :stats="getStats(advertiser.container_id)"
          @click="goToAdvertiser(advertiser.id)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import HealthStatus from '../components/HealthStatus.vue'
import AdvertiserCard from '../components/AdvertiserCard.vue'

export default {
  name: 'Dashboard',
  components: {
    HealthStatus,
    AdvertiserCard
  },
  setup() {
    const router = useRouter()
    const advertisers = ref([])
    const health = ref(null)
    const containersHealth = ref([])
    const loading = ref(false)

    const loadData = async () => {
      loading.value = true
      try {
        const [advertisersRes, healthRes, containersRes] = await Promise.all([
          api.getAdvertisers(),
          api.getHealth(),
          api.getContainersHealth()
        ])
        advertisers.value = advertisersRes.data
        health.value = healthRes.data
        containersHealth.value = containersRes.data
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        loading.value = false
      }
    }

    const getStats = (containerId) => {
      return containersHealth.value.find(c => c.container_id === containerId) || null
    }

    const goToAdvertiser = (id) => {
      router.push(`/advertisers/${id}`)
    }

    onMounted(() => {
      loadData()
    })

    return {
      advertisers,
      health,
      loading,
      getStats,
      goToAdvertiser
    }
  }
}
</script>

<style scoped>
.dashboard h2 {
  margin-bottom: 30px;
  color: #2c3e50;
}

.advertisers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>
