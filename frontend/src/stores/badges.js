import { defineStore } from 'pinia'
import { badgesAPI } from '../api'

const emptyDefinitions = () => ({
  time: { name: '时间里程碑', badges: [] },
  streak: { name: '签到连续', badges: [] },
  special: { name: '特殊成就', badges: [] }
})

export const useBadgesStore = defineStore('badges', {
  state: () => ({
    badges: [],
    allDefinitions: emptyDefinitions()
  }),

  getters: {
    earnedBadges: (state) => state.badges,
    earnedCount: (state) => state.badges.length,
    totalCount: (state) => Object.values(state.allDefinitions)
      .reduce((count, category) => count + category.badges.length, 0)
  },

  actions: {
    async fetchBadges() {
      try {
        const response = await badgesAPI.getList()
        this.badges = response.data
      } catch (error) {
        console.error('Fetch badges error:', error)
        throw error
      }
    },

    async fetchAllDefinitions() {
      try {
        const response = await badgesAPI.getDefinitions()
        this.allDefinitions = response.data
      } catch (error) {
        console.error('Fetch definitions error:', error)
        throw error
      }
    },

    addNewBadge(badge) {
      this.badges.push(badge)
    }
  }
})
