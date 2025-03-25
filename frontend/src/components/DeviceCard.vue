<template>
  <div class="card-container">
    <!-- Карточка в обычном режиме -->
    <div class="card" ref="card">
      <!-- Иконка "три точки" в правом верхнем углу -->
      <button class="more-icon" @click="openFullscreen">
        <i class="fas fa-ellipsis-v"></i> <!-- Используйте Font Awesome или любой другой иконочный шрифт -->
      </button>

      <!-- Содержимое карточки -->
      <div ref="buttonsContainer" class="buttons-container">
        <div v-html="device.html"></div>
      </div>
    </div>

    <!-- Модальное окно для полноэкранного просмотра -->
    <div
      v-if="isFullscreen"
      class="fullscreen-modal"
      @click="closeFullscreen"
      :style="{ display: isFullscreen ? 'flex' : 'none' }"
    >
      <div class="fullscreen-card" @click.stop>
        <!-- Контент карточки в полноэкранном режиме -->
        <div ref="buttonsContainer" class="buttons-container">
          <div v-html="device.html"></div>
        </div>
        <!-- Кнопка закрытия модального окна -->
        <button class="close-button" @click="closeFullscreen">
          <i class="fas fa-times"></i> <!-- Закрывающая иконка -->
        </button>
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
    socket: null,
    isFullscreen: false
  };
},
created() {
  // Установка соединения с вебсокетом при создании компонента
  this.connectWebSocket();
},
beforeUnmount() {
  // Закрытие соединения при уничтожении компонента
  if (this.socket) {
    this.socket.close();
  }
},
mounted() {
    this.addEventListeners();
},
updated() {
    this.addEventListeners();
},
methods: {
    openFullscreen() {
      this.isFullscreen = true; // Включаем полноэкранный режим
    },
    closeFullscreen() {
      this.isFullscreen = false; // Выключаем полноэкранный режим
    },
  addEventListeners() {
    this.$nextTick(() => {
      const container = this.$refs.buttonsContainer;
      if (!container) return;

      // Находим все дочерние элементы с кнопками
      const buttonElements = Array.from(container.children);

      // Сопоставляем HTML-элементы с объектами кнопок
      buttonElements.forEach((element, index) => {
        const button = this.device.buttons[index]; // Получаем соответствующий объект кнопки

        // Удаляем предыдущие обработчики событий
        element.removeEventListener("mousedown", this.startSendingMessages);
        element.removeEventListener("mouseup", this.stopSendingMessages);
        element.removeEventListener("mouseleave", this.stopSendingMessages);

        // Добавляем новые обработчики, передавая объект кнопки
        element.addEventListener("mousedown", () => this.startSendingMessages(button));
        element.addEventListener("mouseup", () => this.stopSendingMessages(button));
        element.addEventListener("mouseleave", () => this.stopSendingMessages(button));

                // Обработчики для мобильных устройств
        element.addEventListener("touchstart", (event) => {
          event.preventDefault();
          this.startSendingMessages(button);
        });
        element.addEventListener("touchend", (event) => {
          event.preventDefault();
          this.stopSendingMessages(button);
        });
        element.addEventListener("touchcancel", (event) => {
          event.preventDefault();
          this.stopSendingMessages(button);
        });

      });
    });
  },
  connectWebSocket() {
    // Замените URL на ваш WebSocket-сервер
    this.socket = new WebSocket('ws://0.0.0.0:8000/button');

    // Обработчик открытия соединения
    this.socket.onopen = () => {
      console.log('Соединение с вебсокетом установлено');
    };

    // Обработчик получения сообщений
    this.socket.onmessage = (event) => {
      const data = event.data;
      console.log('Получено сообщение:', data);

      // Обновление состояния устройства при получении данных
      if (data.deviceId === this.device.id) {
        this.$emit('update:status', data.status); // Обновляем статус через родителя
      }
    };

    // Обработчик ошибок
    this.socket.onerror = (error) => {
      console.error('Ошибка вебсокета:', error);
    };

    // Обработчик закрытия соединения
    this.socket.onclose = () => {
      console.log('Соединение с вебсокетом закрыто');
    };
  },
  startSendingMessages(button) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('Вебсокет не подключен');
      return;
    }

    // Очищаем предыдущий интервал, если он существует
    this.stopSendingMessages();
    const state = button.states[0]
    // Начинаем отправку сообщений каждые 500 мс
    this.sendInterval = setInterval(() => {

      const message = {
        id: state.id,
        protocol: this.device.protocolType
      };

      console.log(this.device.buttons)
      console.log(this.device)
      console.log(button.id)


      this.socket.send(JSON.stringify(message));
      console.log('Отправлено сообщение:', message);
    }, state.time * 1000); // Интервал отправки (500 мс)
  },
  stopSendingMessages() {
    if (this.sendInterval) {
      clearInterval(this.sendInterval); // Останавливаем интервал
      this.sendInterval = null;

      // Отправляем финальное сообщение при отпускании кнопки
//      const message = "Stoop"
        //      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        //        this.socket.send(message);
        //        console.log('Отправлено финальное сообщение:', message);
        //      }
    }
  },
  toggleStatus() {
    // Отправляем команду изменения статуса через вебсокет
    console.log('Отправка команды изменения статуса');

    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('Вебсокет не подключен');
      return;
    }

    // Отправляем новое состояние на сервер
    const newStatus = !this.device.status;
    this.socket.send("Привет Аня!")


    // Опционально: временно обновляем состояние локально
    this.$emit('update:status', newStatus);
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
.card-container {
  position: relative;
  width: 100%;
  max-width: 300px; /* Размер обычной карточки */
  margin: 10px 0; /* Убираем центрирование по горизонтали */
}

.card {
  position: relative;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Иконка "три точки" */
.more-icon {
  position: absolute;
  top: 8px;
  right: 8px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #555;
}

/* Модальное окно */
.fullscreen-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* Полупрозрачный фон */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.fullscreen-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  max-width: 80%; /* Размер карточки в полноэкранном режиме */
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  position: relative;
}

/* Кнопка закрытия модального окна */
.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #555;
}
</style>