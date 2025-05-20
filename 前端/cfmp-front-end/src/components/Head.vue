

<template>
  <div class="root-head">
    <div class="left">
      <h1 class="title" @click="toHomePage">
        校园跳蚤市场管理系统
      </h1>
    </div>

  <div class="right">

    <el-col :span="12">
      <div class="demo-basic--circle" style="padding-right: 50px;padding-left: 10px">
        <div class="block">
          <el-avatar :size="65" :src=headImg v-if="headImg"/>
          <el-avatar :size="65"  v-else @click="toUploadImg" style="cursor: pointer">选择头像</el-avatar>
        </div>
      </div>
    </el-col>
      <a class="username" v-if="userName">
      用户名:{{userName}}
    </a>
    <el-button v-else style="margin: auto;" @click="toLogin">
      登录
    </el-button>
  </div>
</div>

</template>
<script setup>
  import vue from "../assets/vue.svg";
  import {UserInfoStore} from "../stores/userInfo.js";
  import {ref} from "vue";
  const userInfoStore = UserInfoStore();
  let userName = userInfoStore.username
  let headImg = userInfoStore.headImg
  let toLogin = () => {
    console.log("toLogin")
  }
  let toUploadImg = () => {
    console.log("toUploadImg")
  }
  let toHomePage = () => {
    console.log("toHomePage")
  }
</script>
<style scoped>
.root-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background: yellow;
}
.username{
  font-size: 20px;
  font-weight: bold;
  margin: auto;
  padding-right: 10px;
  width: 200px;
}
 .left {
   margin-left: 80px;
   display: flex;
   flex-direction: row;
  }
  .right {
    display: flex;
    margin-right: 10px;
    flex-direction: row-reverse;
  }
  .title{
    font-size: 40px;
    cursor: pointer;
  }
</style>