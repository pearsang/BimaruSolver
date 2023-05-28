import './assets/main.css'

import { createApp } from "vue";
import App from "./App.vue";

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi-svg";
import "@mdi/font/css/materialdesignicons.css";
import router from "./router/index.js";

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    iconfont: "mdiSvg",
    values: {
      mdi,
    },
  },
  
});

createApp(App).use(vuetify).use(router).mount("#app");
