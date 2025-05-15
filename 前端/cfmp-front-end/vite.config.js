import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import * as http from "http";

// https://vitejs.dev/config/
export default defineConfig(
  () => {
    return{
      plugins: [vue()],
       // 这个不用一点点写, 但每个配置都要理解
    server: {
          port: 5173,
    open: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true, // 表示开启代理, 允许跨域请求数据
        secure: false, // 如果是https接口，需要配置这个参数
        agent: new http.Agent(),
      },
    },
  }
    }
  }
 )
