<script setup>
<<<<<<< HEAD
// 这里可以放置全局逻辑（如需）
</script>

<template>
  <!-- 简化版路由视图容器 -->
  <router-view />
=======
import HelloWorld from './components/HelloWorld.vue'
import { RouterView } from 'vue-router'
</script>

<template>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <RouterView/>
>>>>>>> 11b53feeb6e16b34efa49e9a9e53ae43242ac49b
</template>

<style>
/* 全局基础样式 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 
               'Segoe UI', 'PingFang SC', 'Microsoft YaHei',
               sans-serif;
  margin: 0;
  color: #333;  /* 更易读的文字颜色 */
  background: #ffffff; /* 明确设置白色背景 */
}

/* 移除所有过渡动画相关样式 */
</style>

<style scoped>
/* 组件级样式（如需） */
/* 空内容表示不需要组件级样式 */
</style>