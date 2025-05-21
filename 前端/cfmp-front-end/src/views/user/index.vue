<script setup>
import  LeftBar  from '../../components/user/leftbar.vue'
import Head from '../../components/Head.vue'
</script>

<template>
  <Head></Head>
<div class="container">
      <!-- 左侧导航 -->
      <aside class="left-sidebar">
        <LeftBar />
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
        <router-view />
      </main>
    </div>

</template>

<style scoped>
.header {
  height: 100px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
.left-sidebar {
  width: 16%;
  background: #ffffff;
  overflow-y: auto;
  height: 100vh;

}
.container {
  flex: 1;
  display: flex;
  overflow: hidden;
  width: 100%;
}

.main-content {
  flex: 1;
  padding-top: 20px;
  padding-left: 20px;
  overflow-y: auto;
  background: #fff;
  width: 60%;
}
</style>