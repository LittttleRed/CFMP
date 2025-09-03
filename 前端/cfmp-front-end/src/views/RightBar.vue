<template>
  <!-- 固定定位组件 -->
  <div class="fixed-component">
    <el-button class="right-button" @click="toLaunch">发闲置</el-button>
    <hr>
    <el-button class="right-button" @click="chat">消息</el-button>
    <hr>
    <el-button class="right-button" @click="toHomePage">主页</el-button>
    <hr>
    <el-button class="right-button" @click="toTop">回顶部</el-button>
  </div>
<el-dialog
  class="friend-list"
  :modal="false"
  draggable
  style="width: 400px; height: 700px;background-color: #fffded"
  v-model="chating"
>
  <!-- 顶部用户信息（固定高度） -->
  <div class="user">
    <el-avatar :size="70" :src="getHeadImg()" shape="square"></el-avatar>
    <div class="username">{{ getUserName() }}</div>
  </div>

  <!-- 消息标题（固定高度） -->
  <div style="display: flex;flex-direction: row">
  <div style="cursor: pointer;font-size: 20px; margin: 20px 0 10px 10px; " @click="toFollower" :style="infollower ? 'color : #ffa78a' : ''">我关注的</div>
  <div style="cursor: pointer;font-size: 20px; margin: 20px 0 10px 20px" @click="toFollowee" :style="infollowee ? 'color : #ffa78a' : ''">关注我的</div>
    <div style="cursor: pointer;font-size: 20px; margin: 20px 0 10px 20px" @click="toSystem">系统通知</div>
    </div>
  <hr>

  <!-- 可滚动聊天列表区域 -->
  <div class="scrollable-chat-list">
    <el-scrollbar style="height: 500px">
      <div class="chat-list">
        <el-card
          class="chat-item"
          v-for="item in chatList"
          :key="item.user_id"
          style="margin-bottom: 10px"
          @click="openChat(item.user_id)"
        >
          <div class="user">
            <el-avatar :size="50" :src="item.avatar" shape="square"></el-avatar>
            <div class="chatername">{{ item.username }}</div>
          </div>
        </el-card>
      </div>
    </el-scrollbar>
  </div>
</el-dialog>

  <el-dialog class="chat" draggable v-model="Chater" style="height: 900px;width: 900px">
      <chat-content v-if="Chater" :user-id="currentChatUserId" style="margin-bottom: 0"></chat-content>
  </el-dialog>
  <el-dialog class="chat" draggable v-model="System" style="height: 900px;width: 900px;--el-dialog-border-radius: 20px">
     <Systemchat  v-if="System" style="margin-bottom: 0"></Systemchat>
  </el-dialog>
  <!-- 占位容器（仅演示用） -->
</template>

<script setup>
import {ref} from "vue";
import ChatContent from "@/views/chat/chatcontent.vue";
import {getHeadImg, getToken, getUserName} from "@/utils/user-utils.js";
import {getAllFollowees, getAllFollows} from "@/api/user/index.js";
import {ElMessage} from "element-plus";
import Systemchat from "./chat/systemchat.vue"

const chating = ref(false);
const follower = ref([]);//我关注的
const followee = ref([]);//关注我的
const  chatList = ref([]);
const Chater = ref(false);  // 修改为布尔值
const currentChatUserId = ref(''); // 新增用于存储当前聊天用户ID
const System = ref(false);
const infollower=ref(false)
const infollowee=ref(false);
const getFollower = async () => {
  await getAllFollows(getToken()).then(ref => {
    follower.value = ref.map(item =>item.followee)
    console.log(ref)
    console.log(chatList.value)
  })
}
const getFollowee = async () => {
    await getAllFollowees(getToken()).then(
      ref=>{
        followee.value = ref.map(item =>item.follower)
      }
  )
}
const chat= async ()=>{
  if(getToken()) {
    chating.value = true
    await getFollowee();
    await getFollower();
    chatList.value = follower.value
    console.log(chatList.value)
    console.log(followee.value)
  }else{
    ElMessage("请先登录")
  }
}
const toFollower=()=>{
  infollower.value=true
  infollowee.value=false
  chatList.value = follower.value
}
const toFollowee=()=>{
    infollower.value=false
  infollowee.value=true
  chatList.value = followee.value
}
const toSystem=()=>{
  System.value = true
}
const buildWenSocket = () => {

}

const openChat = (userId) => {
  currentChatUserId.value = userId;
  Chater.value = true;
}

const toHomePage = () => {
   window.location.href = "/user"
};
const toTop = () => {
  window.scrollTo(0, 0);
};
const toLaunch = () => {
  if(getToken()){
  window.location.href = "/product/launch"}
  else{
    ElMessage("请先登录")
  }
};
</script>

<style scoped>
.friend-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 可滚动区域（关键样式） */
.scrollable-chat-list {
  flex: 0.5; /* 占据剩余空间 */
  overflow: hidden; /* 隐藏原生滚动条 */
  margin-top: 10px;
}

/* Element Plus 滚动条样式调整 */
:deep(.el-scrollbar) {
  height: 100%;
}

:deep(.el-scrollbar__wrap) {
  overflow-x: hidden; /* 隐藏横向滚动 */
}

/* 聊天列表布局 */
.chat-list {
  padding-right: 10px; /* 避免内容紧贴滚动条 */
}

/* 聊天项样式 */
.chat-item {
  cursor: pointer;
  transition: all 0.3s;
  height: 80px;
}
.chat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.chatername{
  margin-left:5px;
  font-size: 22px;
  font-weight: bold;
}
/* 用户信息展示样式 */
.user {
  display: flex;
  align-items: center;
  gap: 15px;
}
.username {
  font-size: 16px;
  font-weight: 500;
}
/* 基础固定定位样式 */
.user{
  display: flex;
  flex-direction: row;
}
.username{
  font-size: 30px;
  font-weight: bold;
  margin-top: 5px;
  margin-left: 10px;
}
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
.friend-list{
  width: 400px;
  height: 700px;
  display: flex;
  flex-direction: column;
}
</style>