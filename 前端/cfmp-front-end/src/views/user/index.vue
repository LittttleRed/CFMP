<template>
  <Head></Head>
<div class="container">
      <!-- 左侧导航 -->
      <aside class="left-sidebar">
        <LeftBar :is-my-home="isMyHome"/>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
          <div class="left" v-if="!route.fullPath.endsWith('setting')">
            <el-avatar   :size="120" v-if="avatar.value!==''" :src="avatar"></el-avatar>
            <el-avatar  :size="120" v-else src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
            <div class="info" style="margin-top: 20px;margin-bottom: 30px;margin-left: 50px;font-weight: bold;font-size: 30px">
              {{ username }}
              <div>
                <el-button style="margin: 20px auto" v-if="!isMyHome&&!hadfollowed" @click="follow">关注</el-button>
                <el-button style="margin-left: 20px;" type="danger" v-if="!isMyHome&&hadfollowed" @click="unfollow">取消关注</el-button>
                <el-button style="margin-left: 20px;" type="danger" v-if="!isMyHome" @click="complaintdialog = true">举报</el-button>
              </div>
            </div>
          </div>
        <router-view />
      </main>
 <el-dialog v-model="complaintdialog" title="举报">
      <el-form>
          <el-form-item  style="width: 100%;height: 200px">
              <el-input type="textarea" :rows="6" v-model="complaintContent" placeholder="请输入举报内容"></el-input>
            </el-form-item>
        <el-button type="primary" @click="complaintdialog = false">取消</el-button>
        <el-button type="primary" @click="complaint">提交</el-button>
      </el-form>
    </el-dialog>
</div>

</template>
<script setup>
import  LeftBar  from '../../components/user/leftbar.vue'
import Head from '../../components/Head.vue'
import {ref, watch} from "vue";
import {useRoute, useRouter} from "vue-router";
import {getHeadImg, getToken, getUserId} from "../../utils/user-utils.js";
import {createComplaint, followUser, getAllFollows, getMe, getUserById, unfollowUser} from "../../api/user/index.js";
import {ElMessage} from "element-plus";
const username = ref('123214213123')
const avatar = ref('')
const route = useRoute()
const touter = useRouter()
const isMyHome = ref(false)
const hadfollowed  = ref(false)
const complaintdialog = ref(false)
const complaintContent = ref('')
if(route.query.user_id === getUserId() || route.query.user_id === undefined){
  isMyHome.value = true
}
const isfollowee = async() =>{
 await getAllFollows(getToken()).then(res => {
   console.log(res)
   for(let i=0;i<res.length;i++){
     if(res[i]["followee"]==route.query.user_id){
       hadfollowed.value = true
       break
     }
   }
 })
}
isfollowee()
const follow = async () => {
  await followUser(getToken(),route.query.user_id).then(res => {
    ElMessage.success('关注成功')
    hadfollowed.value = true
  })
}
const unfollow = async () => {
  await unfollowUser(getToken(),route.query.user_id).then(res => {
    ElMessage.success('取消关注成功')
    hadfollowed.value = false
  })
}
const getOtherUser=async ()=>{
let response = await getUserById(route.query.user_id).then(
    (response) => {
      username.value=response["username"]
      if(response["avatar"]!==null){
      avatar.value=response["avatar"]
      }
    }
).catch((error)=>{

})
}
const complaint=async ()=>{
   let data = {
    complainer_id: getUserId(),
    target_type: 1,
    target_id: route.query.user_id,
    reason: complaintContent.value,
    status: 0
  }
  await createComplaint(getToken(),data).then(res => {
    ElMessage.success('举报成功')
    complaintdialog.value = false
  })
}
const getMySelf=async ()=>{
let token = getToken()
await getMe(token).then((response) => {
  let user=response[0]
  console.log(user["avatar"])
  username.value=user["username"]
  avatar.value=user["avatar"]
})
}
if(isMyHome.value===true){
  console.log("我")
getMySelf()
}else{
getOtherUser()
}
</script>
<style scoped>
.info{
  display: flex;
  flex-direction: column;
}
.left{
  display: flex;
  flex-direction: row;
}
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