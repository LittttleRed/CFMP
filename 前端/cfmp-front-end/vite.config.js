import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import * as http from "http";
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig(
  () => {
    // 判断是否在Docker环境中运行
    const isDocker = process.env.DOCKER_ENV === 'true';
    
    return{
      plugins: [vue()],
      resolve: {
        alias: {
          '@': resolve(__dirname, 'src')
        }
      },
       // 这个不用一点点写, 但每个配置都要理解
    server: {
          port: 5173,
          host: '0.0.0.0', // 允许从外部访问
          open: !isDocker, // 在Docker环境中不自动打开浏览器
          proxy: {
            "/api": {
              target: isDocker ? "http://backend:8000" : "http://127.0.0.1:8000",
              changeOrigin: true, // 表示开启代理, 允许跨域请求数据
              secure: false, // 如果是https接口，需要配置这个参数
              agent: new http.Agent(),
            },
              "/minio":{
                target: "http://59.110.23.64:9000",
                  changeOrigin: true,
                  secure: false,
                  agent: new http.Agent(),
                  rewrite: (path) => path.replace(/^\/minio/, ""),
              }
          },
    }
    }
  }
 )
