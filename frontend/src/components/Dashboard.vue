<template>
  <div class="dashboard">
    <!-- Хэдер -->
    <header class="bg-dark text-white py-3">
      <div class="container">
        <h1 class="text-center">Умный дом</h1>
        <nav class="d-flex justify-content-center">
          <ul class="nav nav-pills">
            <li class="nav-item">
              <router-link to="/" class="nav-link active">Главная</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/devices" class="nav-link">Устройства</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/settings" class="nav-link">Настройки</router-link>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <!-- Основной контент -->
    <main class="container my-5">
      <h2 class="mb-4">Устройства</h2>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <!-- Карточки устройств -->
        <DeviceCard
          v-for="(device, index) in devices"
          :key="index"
          :device="device"
        />
      </div>
    </main>
  </div>
</template>

<script>
import DeviceCard from './DeviceCard.vue';

export default {
  name: 'MainDashboard',
  components: {
    DeviceCard,
  },
  data() {
    return {
      // Массив устройств
      devices: [
        {
          id: 1,
          name: 'Лампа спальни',
          type: 'light',
          status: true,
          icon: 'https://via.placeholder.com/50?text=lamp',
        },
        {
          id: 2,
          name: 'Терmostat',
          type: 'thermostat',
          status: false,
          temperature: 22,
          icon: 'https://via.placeholder.com/50?text=thermo',
        },
        {
          id: 3,
          name: 'Камера',
          type: 'camera',
          status: true,
          icon: 'https://via.placeholder.com/50?text=camera',
        },
        // Добавьте больше устройств...
      ],
    };
  },
};
</script>

<style scoped>
.dashboard {
  font-family: Arial, sans-serif;
}

.header {
  background-color: #343a40 !important;
  color: white;
}

.nav-pills .nav-link.active {
  background-color: #007bff !important;
}

.content {
  margin-top: 20px;
}
</style>