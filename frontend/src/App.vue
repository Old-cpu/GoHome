<template>
  <div id="app">
    <nav class="navbar" v-if="showNav">
      <div class="nav-container">
        <router-link to="/" class="logo">思乡签到</router-link>
        <div class="nav-links">
          <router-link to="/dashboard">首页</router-link>
          <router-link to="/checkin">签到</router-link>
          <router-link to="/badges">勋章</router-link>
          <router-link to="/profile">我的</router-link>
          <button type="button" class="nav-logout" @click="handleLogout">退出登录</button>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from './stores/user'
import { useCheckinStore } from './stores/checkin'
import { useBadgesStore } from './stores/badges'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const checkinStore = useCheckinStore()
const badgesStore = useBadgesStore()
const showNav = computed(() => !['/login', '/register'].includes(route.path))

const handleLogout = async () => {
  await userStore.logout()
  checkinStore.$reset()
  badgesStore.$reset()
  router.push('/login')
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: #FAF8F5;
}

.navbar {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.06);
  padding: 12px 0;
}

.nav-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #F5A623;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links a,
.nav-logout {
  color: #333;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-logout:hover {
  color: #F5A623;
}

.nav-logout {
  background: transparent;
  border: 0;
  cursor: pointer;
  font: inherit;
  padding: 0;
}

.main-content {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 20px;
}

@media (max-width: 640px) {
  .nav-container {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;
  }

  .nav-links {
    flex-wrap: wrap;
    gap: 12px 18px;
  }
}
</style>
