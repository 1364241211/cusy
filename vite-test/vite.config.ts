import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import {
  ElementPlusResolver,
  VantResolver,
} from "unplugin-vue-components/resolvers";
import legacy from "@vitejs/plugin-legacy";
// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules")) {
            return id
              .toString()
              .split("node_modules/")[1]
              .split("/")[0]
              .toString();
          }
        },
      },
    },
  },
  plugins: [
    vue(),
    AutoImport({
      imports: ["vue", "vue-router"],
      resolvers: [ElementPlusResolver(), VantResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver(), VantResolver()],
    }),
    legacy({
      targets: ["defaults", "not IE 11"],
    }),
  ],
  server: {
    host: "192.168.2.103",
    port: 3000,
    proxy: {
      "/api": {
        target: "192.168.2.103:8000",
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: "192.168.2.103",
    port: 3000,

    proxy: {
      "/api": {
        target: "192.168.2.103:8000",
        changeOrigin: true,
      },
    },
  },
});
