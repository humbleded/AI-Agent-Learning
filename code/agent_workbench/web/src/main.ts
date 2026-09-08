import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { ElAlert, ElButton, ElOption, ElSelect, ElTag } from "element-plus";
import "element-plus/dist/index.css";
import "./style.css";
import "./themes.css";
import { initializeTheme } from "./lib/theme";

const app = createApp(App);
initializeTheme();

app.use(router);
for (const component of [ElAlert, ElButton, ElOption, ElSelect, ElTag])
  app.use(component);

app.mount("#app");
