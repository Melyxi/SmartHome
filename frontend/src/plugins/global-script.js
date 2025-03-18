export default {
  install(app) {
    let scriptLoaded = false;

    app.config.globalProperties.$loadScript = () => {
      if (!scriptLoaded) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/some-library@latest/dist/some-library.min.js';
        script.onload = () => {
          console.log('Глобальный скрипт загружен!');
          scriptLoaded = true;
        };
        document.body.appendChild(script);
      }
    };
  }
};