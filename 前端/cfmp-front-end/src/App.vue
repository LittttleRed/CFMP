<script setup>
// 这里可以放置全局逻辑（如需）
</script>

<template>
  <!-- 简化版路由视图容器 -->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <router-view />
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

</style>

<style scoped>
/* 组件级样式（如需） */
/* 空内容表示不需要组件级样式 */
</style>