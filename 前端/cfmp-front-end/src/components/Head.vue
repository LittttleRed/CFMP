

<template>
  <div class="root-head">
    <div class="left">
      <h1 class="title" @click="toHomePage">
        校园跳蚤市场
      </h1>
    </div>
<Search v-if="showSearch===true" ></Search>
  <div class="right">

    <el-col :span="12">
      <div class="demo-basic--circle" style="padding-right: 50px;padding-left: 10px" @click="toUserHome">
        <div class="block">
          <el-avatar :size="65" :src=headImg v-if="headImg"/>
          <el-avatar :size="65"  v-else  style="cursor: pointer"  src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
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
  import { useUserStore } from "../stores/user.js";
  import {ref} from "vue";
  import Search from "./home/search.vue";
  const userInfoStore = useUserStore();
  let userName = userInfoStore.username
  let headImg = userInfoStore.avatar
  let toLogin = () => {
    console.log("toLogin")
  }
  let toUserHome = () => {
    console.log("toUserHome")
    window.location.href = "/user"
  }
  let toHomePage = () => {
    console.log("toHomePage")
    window.location.href = "/"
  }
  defineProps({
    showSearch: {
      type: Boolean,
      default: false
    }
  })
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