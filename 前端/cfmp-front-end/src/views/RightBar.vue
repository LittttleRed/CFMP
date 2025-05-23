<template>
  <!-- 固定定位组件 -->
  <div class="fixed-component">
    <el-button class="right-button" @click="toLaunch">发闲置</el-button>
    <hr>
    <el-button class="right-button">消息</el-button>
    <hr>
    <el-button class="right-button" @click="toHomePage">主页</el-button>
    <hr>
    <el-button class="right-button" @click="toTop">回顶部</el-button>
  </div>

  <!-- 占位容器（仅演示用） -->
</template>

<script setup>
const toHomePage = () => {
   window.location.href = "/user"
};
const toTop = () => {
  window.scrollTo(0, 0);
};
const toLaunch = () => {
  window.location.href = "/product/launch"
};
</script>

<style scoped>
/* 基础固定定位样式 */
.fixed-component {
  position: fixed;
  z-index: 1000; /* 确保位于顶层 */
  background: #ffffff;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  border-radius: 40px;
}

/* 动态定位模式 */
.fixed-component {
  top: 300px;
  right: -30px;
  transform: translateX(-50%);
  width: 50px;
  height: 260px;
  flex-direction: column;
}
.right-button{
  margin: 1px auto;
  width: 50px;
  height: 50px;
  border: none;
}
hr{
  border: gainsboro 1px solid;
}
</style>