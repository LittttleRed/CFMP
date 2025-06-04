
<template>
    <Head class="header"></Head>
      <!-- 左侧导航 -->
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
<script setup>
import Head from "../../components/Head.vue";
import LeftBar from "../../components/root/LeftBar.vue";
import user from "./user.vue"
import {getPrivileges} from "@/utils/user-utils.js";
if(getPrivileges()==0){
  window.location.href = "/"
}
</script>

<style scoped>
.header {
  height: 100px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
.left-sidebar {
  width: 15%;
  background: #f5f7fa;
  overflow-y: auto;
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