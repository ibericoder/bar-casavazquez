import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import pinia from './store';
import 'primeicons/primeicons.css';
import './assets/styles/main.scss';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

import { setDefaultOptions } from 'date-fns'
import { de } from 'date-fns/locale'
setDefaultOptions({ locale: de })
const app = createApp(App);

app.use(router);
app.use(pinia);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'system',
            cssLayer: false
        }
    }
});

app.mount('#app');
