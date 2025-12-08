import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    advertisers: [],
    currentAdvertiser: null,
    loading: false,
    error: null
  }),
  
  actions: {
    setAdvertisers(advertisers) {
      this.advertisers = advertisers
    },
    
    setCurrentAdvertiser(advertiser) {
      this.currentAdvertiser = advertiser
    },
    
    setLoading(loading) {
      this.loading = loading
    },
    
    setError(error) {
      this.error = error
    }
  }
})
