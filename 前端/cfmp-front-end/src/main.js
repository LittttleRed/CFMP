import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import router from './router'
import 'element-plus/dist/index.css'
import App from './App.vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import pinia from './stores/index.js'
const app = createApp(App)

app.use(ElementPlus, {
    locale: zhCn,
})
app.use(router)
app.use(pinia)
app.mount('#app')