import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Advertisers
  getAdvertisers() {
    return api.get('/advertisers')
  },
  getAdvertiser(id) {
    return api.get(`/advertisers/${id}`)
  },
  createAdvertiser(data) {
    return api.post('/advertisers', data)
  },
  updateAdvertiser(id, data) {
    return api.put(`/advertisers/${id}`, data)
  },
  deleteAdvertiser(id) {
    return api.delete(`/advertisers/${id}`)
  },
  getAdvertiserCode(id) {
    return api.get(`/advertisers/${id}/code`)
  },
  getAdvertiserStats(id) {
    return api.get(`/advertisers/${id}/stats`)
  },

  // Scripts (Global)
  getScripts() {
    return api.get('/scripts')
  },
  getScript(id) {
    return api.get(`/scripts/${id}`)
  },
  createScript(data) {
    return api.post('/scripts', data)
  },
  updateScript(id, data) {
    return api.put(`/scripts/${id}`, data)
  },
  deleteScript(id) {
    return api.delete(`/scripts/${id}`)
  },
  toggleScript(id) {
    return api.patch(`/scripts/${id}/toggle`)
  },

  // Advertiser Scripts
  getAdvertiserScripts(advertiserId) {
    return api.get(`/advertisers/${advertiserId}/scripts`)
  },
  createAdvertiserScript(advertiserId, data) {
    return api.post(`/advertisers/${advertiserId}/scripts`, data)
  },
  updateAdvertiserScript(advertiserId, scriptId, data) {
    return api.put(`/advertisers/${advertiserId}/scripts/${scriptId}`, data)
  },
  deleteAdvertiserScript(advertiserId, scriptId) {
    return api.delete(`/advertisers/${advertiserId}/scripts/${scriptId}`)
  },
  toggleAdvertiserScript(advertiserId, scriptId) {
    return api.patch(`/advertisers/${advertiserId}/scripts/${scriptId}/toggle`)
  },

  // Health
  getHealth() {
    return api.get('/health')
  },
  getContainersHealth() {
    return api.get('/health/containers')
  },
  getContainerLogs(advertiserId) {
    return api.get(`/health/containers/${advertiserId}/logs`)
  }
}
