<template>
  <div class="col">
    <div class="card h-100 shadow-sm">
      <img :src="localDevice.icon" :alt="localDevice.name" class="card-img-top" />
      <div class="card-body">
        <h5 class="card-title">{{ localDevice.name }}</h5>
        <p class="card-text">
          <strong>Статус:</strong>
          <span :class="statusClass">{{ localDevice.status ? 'Включено' : 'Выключено' }}</span>
        </p>
        <button
          v-if="localDevice.type === 'light'"
          class="btn btn-primary w-100"
          @click="toggleStatus"
        >
          {{ localDevice.status ? 'Выключить' : 'Включить' }}
        </button>
        <div v-if="localDevice.type === 'thermostat'" class="input-group mb-3">
          <input
            type="number"
            class="form-control"
            placeholder="Температура"
            v-model="localDevice.temperature"
          />
          <button class="btn btn-success" @click="updateTemperature">Обновить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeviceCard',
  props: {
    device: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      // Create a local copy of the device prop
      localDevice: { ...this.device },
    };
  },
  computed: {
    statusClass() {
      return this.localDevice.status ? 'text-success' : 'text-danger';
    },
  },
  watch: {
    // Update the localDevice if the prop changes
    device: {
      handler(newVal) {
        this.localDevice = { ...newVal };
      },
      deep: true,
    },
  },
  methods: {
    toggleStatus() {
      // Emit an event to update the parent component
      this.$emit('update:status', !this.localDevice.status);
    },
    updateTemperature() {
      // Emit an event to notify the parent component of the temperature change
      this.$emit('update:temperature', this.localDevice.temperature);
      alert(`Температура изменена на ${this.localDevice.temperature}°C`);
    },
  },
};
</script>

<style scoped>
.text-success {
  color: #28a745;
}
.text-danger {
  color: #dc3545;
}
.card {
  border-color: #ddd;
}
.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>