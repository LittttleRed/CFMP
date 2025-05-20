import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import router from './router'
import 'element-plus/dist/index.css'
import App from './App.vue'
<<<<<<< HEAD
import router from './router'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.use(createPinia())
app.mount('#app')
=======
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import pinia from './stores/index.js'
const app = createApp(App)

app.use(ElementPlus, {
    locale: zhCn,
})
app.use(router)
app.use(pinia)
app.mount('#app')
>>>>>>> 11b53feeb6e16b34efa49e9a9e53ae43242ac49b
