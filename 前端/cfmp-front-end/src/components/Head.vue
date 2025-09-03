

<template>
  <div class="root-head">
    <div class="left">
      <h1 class="title" @click="toHomePage">
        校园跳蚤市场
      </h1>

    </div>
<Search v-if="showSearch===true" style="border-radius: 40px;" ></Search>
  <div class="right">

    <el-col :span="12">
      <div class="demo-basic--circle" style="padding-right: 50px;padding-left: 10px" @click="toUserHome">
        <div class="block">
          <el-avatar :size="65" :src=headImg v-if="headImg!=null"/>
          <el-avatar :size="65"  v-else-if="getPrivileges()==1"  style="cursor: pointer"  src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
          <el-avatar :size="65"  v-else style="cursor: pointer"  src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
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
  import {reactive, ref, watch} from "vue";
  import Search from "./home/search.vue";
  import {storeToRefs} from "pinia";
  import {getHeadImg, getPrivileges, getUserName} from "../utils/user-utils.js";
  const userInfoStore = useUserStore();
  let userName = getUserName()
  let headImg = getHeadImg()

  console.log(headImg)
  let toLogin = () => {
    console.log("toLogin")
    window.location.href = "/login"
  }
  let toUserHome = () => {
    console.log("toUserHome")

    if(getPrivileges()==0)
    window.location.href = "/user"
  }
  let toHomePage = () => {
    console.log("toHomePage")
    if(getPrivileges()==1){
      window.location.href = "/root"
    }else {
      window.location.href = "/"
    }
  }
  defineProps({
    showSearch: {
      type: Boolean,
      default: false
    }
  })
const initUserInfo = () => {

  }
</script>
<style scoped>
.root-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background: yellow;
  height: 35%;
}
.username{
  font-size: 20px;
  font-weight: bold;
  margin: auto;
  padding-right: 10px;
  width: 300px;
}
 .left {
   margin-left: 5%;
   display: flex;
   flex-direction: row;

  }
  .right {
    display: flex;
    margin-right: 10%;
    flex-direction: row-reverse;
  }
  .title{
    font-size: 3vh;
    cursor: pointer;
    margin-right: 50px;
    width: 150px;
  }
</style>