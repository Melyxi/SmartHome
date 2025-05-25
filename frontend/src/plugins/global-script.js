export default {
  install(app) {
    const loadedResources = new Set();

    app.config.globalProperties.$loadResources = async () => {
      const resources = [
        {
          type: 'script',
          url: 'https://cdn.jsdelivr.net/npm/some-library@latest/dist/some-library.min.js'
        },
        {
          type: 'style',
          url: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
        }
      ];

      const loadPromises = resources
        .filter(resource => !loadedResources.has(resource.url))
        .map(resource => {
          return new Promise((resolve, reject) => {
            if (resource.type === 'script') {
              const script = document.createElement('script');
              script.src = resource.url;
              script.onload = () => {
                loadedResources.add(resource.url);
                resolve();
              };
              script.onerror = reject;
              document.body.appendChild(script);
            } else if (resource.type === 'style') {
              const link = document.createElement('link');
              link.rel = 'stylesheet';
              link.href = resource.url;
              link.onload = () => {
                loadedResources.add(resource.url);
                resolve();
              };
              link.onerror = reject;
              document.head.appendChild(link);
            }
          });
        });

      try {
        await Promise.all(loadPromises);
        console.log('Все ресурсы загружены');
      } catch (error) {
        console.error('Ошибка загрузки ресурсов:', error);
        throw error;
      }
    };
  }
};