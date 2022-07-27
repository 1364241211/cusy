import { createApp } from "vue";
import App from "./App.vue";
import "element-plus/theme-chalk/src/message.scss";
import "element-plus/theme-chalk/src/table.scss";
import "element-plus/theme-chalk/src/message-box.scss";
import "element-plus/theme-chalk/src/popover.scss";
import "element-plus/theme-chalk/src/popconfirm.scss";
import "element-plus/theme-chalk/src/popper.scss";
import "element-plus/theme-chalk/src/overlay.scss";
import "element-plus/theme-chalk/src/form-item.scss";
import "element-plus/theme-chalk/src/form.scss";

import "vant/es/notify/style/index";
import "vant/es/empty/style/index"

import { Tabs, Tab } from "vant";

import { createPinia } from "pinia";
import router from "./router";

import * as Icons from "@element-plus/icons";
const pinia = createPinia();

const app = createApp(App);

app.use(pinia).use(router);
app.use(Tab).use(Tabs);
app.mount("#app");
// // 创建Icon组件
// const Icon = (props: { icon: string }) => {
//     const { icon } = props
//     return createVNode(Icons[icon as keyof typeof Icons])
// }
// // 注册Icon组件
// app.component('Icon', Icon)
Object.keys(Icons).forEach((key) => {
  app.component(key, Icons[key as keyof typeof Icons]);
});
