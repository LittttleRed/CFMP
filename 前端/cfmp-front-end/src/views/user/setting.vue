<template>
  <el-card class="profile-card">
    <div class="profile-container">
      <!-- 头像区域 -->
      <div class="avatar-section">
        <el-avatar
          :size="120"
          :src="avatar"
          class="user-avatar"
        >
          <i class="el-icon-user-solid" v-if="!avatar" >选择头像</i>
        </el-avatar>
        <el-button
          type="primary"
          class="edit-btn"
          @click="this.$refs.fileInput.click()"
        >
          修改头像
        </el-button>
        <input
      type="file"
      accept="image/*"
      @change="changeAvatar"
      ref="fileInput"
      class="edit-btn"
      style="display: none"
    />
        <div v-if="error" class="error-message">{{ error }}</div>
      </div>

      <!-- 信息区域 -->
      <div class="info-section">
        <div class="info-item">
          <label class="info-label">用户名：</label>
          <span class="info-content" v-if="nameChanging===false">{{ userStore.username }}</span>
          <el-input
            v-model="userStore.username"
            placeholder="请输入用户名"
            class="qqmail-input"
            v-if="nameChanging"
            width="100px"
          ></el-input>
          <el-button @click="rejectName" v-if="nameChanging" style="margin-left: 10px">取消</el-button>
          <el-button @click="ensureName" v-if="nameChanging">确定</el-button>
          <el-button @click="changeName">修改用户名</el-button>
        </div>

        <div class="info-item">
          <label class="info-label">电子邮箱：</label>
          <span class="info-content">{{ email }}</span>
          <el-button @click="changeEmail">修改电子邮箱</el-button>
        </div>
        <div class="info-item">
          <label class="info-label">我的地址：</label>
          <span class="info-content" v-if="addressChanging===false">{{ address }}</span>
          <el-input
            v-model="address"
            placeholder="请输入地址"
            class="qqmail-input"
            v-if="addressChanging"
            width="100px"
          ></el-input>
          <el-button @click="rejectAddr" v-if="addressChanging" style="margin-left: 10px">取消</el-button>
          <el-button @click="ensureAddr" v-if="addressChanging">确定</el-button>
          <el-button @click="changeAddr">修改地址</el-button>
        </div>
        <el-button style="width: 20%" @click="changepwd">修改密码</el-button>
        <el-button style="width: 20%;margin-left: 0" @click="logout">退出登录</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import {useUserStore} from '../../stores/user.js'
import {onMounted, ref,watch} from 'vue'
import {
  getToken,
  removeHeadImg,
  removeToken,
  removeUserId,
  removeUserName,
  setHeadImg,
  setUserName
} from "../../utils/user-utils.js";
import * as $api from "../../api/user/index.js";
import {changeUser, getMe, updateAvatar} from "../../api/user/index.js";
import router from "../../router/index.js";
  import { useRouter } from 'vue-router'

let userStore = useUserStore()
const error = ref('')
const emit = defineEmits(['edit'])
const selectedFile = ref(null);
const avatar = ref('')
const nameChanging = ref(false)
const previousName = ref('')
const addressChanging = ref(false)
const preAddr = ref('')
const email = ref('')
const address = ref('')

const logout = ()=>{
  removeToken()
      removeUserName()
      removeUserId()
      removeHeadImg()
  router.push('/')
}
const showinfo=async () => {
  let token = getToken()
  await getMe(token).then((response) => {
    let user=response
    console.log(user)
    userStore.username = user["username"]
    email.value = user["email"]
    avatar.value= user["avatar"]
    address.value = user["address"]
  //去除avatar的"http://127.0.0.1:8000/"前缀
  })
}
showinfo()
const handleEdit = () => {
  emit('edit')
}
const changeAvatar = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 验证文件类型和大小
  if (!file.type.startsWith('image/')) {
    error.value = '请选择图片文件';
    return;
  }
  if (file.size > 2 * 1024 * 1024) {
    error.value = '文件大小不能超过2MB';
    return;
  }
  selectedFile.value = file;
  error.value = '';
  avatar.value = URL.createObjectURL(file);
  let token = getToken()
  
  try {
    const res = await updateAvatar(token, file)
    console.log("头像更新响应:", res)
    // 确保从响应中正确获取头像值
    if (res && res.avatar) {
      avatar.value = res.avatar;
      setHeadImg(res.avatar)
    } else if (res && res.data && res.data.avatar) {
      // 如果响应数据在data字段中
      avatar.value = res.data.avatar;
      setHeadImg(res.data.avatar)
    } else {
      // 如果没有avatar字段，使用原始值
      error.value = '头像更新失败，请重试';
      showinfo() // 恢复原始信息
    }
  } catch (err) {
    // 如果更新失败，恢复原来的头像
    console.error("头像更新失败:", err)
    error.value = '头像更新失败: ' + (err.message || '未知错误');
    // 恢复原始头像
    showinfo()
  }
};
const changeName = () => {
    nameChanging.value=true
    previousName.value=userStore.username
}
const rejectName = () => {
    nameChanging.value=false
    setUserName(previousName.value)
    userStore.username = previousName.value
}
const ensureName = async () => {
  nameChanging.value = false
  let token  = getToken()
  console.log(userStore.username)
  try {
    const res = await changeUser(token, {username: userStore.username})
    // 确保从响应中正确获取用户名
    if (res && res.username) {
      userStore.username = res.username
      setUserName(res.username)
    } else if (res && res.data && res.data.username) {
      // 如果响应数据在data字段中
      userStore.username = res.data.username
      setUserName(res.data.username)
    }
  } catch (error) {
    // 如果更新失败，恢复原来的用户名
    userStore.username = previousName.value
    setUserName(previousName.value)
    console.error("用户名更新失败:", error)
    // 可以添加错误提示
  }
}
const changeAddr=()=>{
  addressChanging.value=true
  preAddr.value=address.value
}
const rejectAddr = () => {
  addressChanging.value = false
  address.value = preAddr.value
}
const ensureAddr = async () => {
  addressChanging.value = false
  let token  = getToken()
  try {
    const res = await changeUser(token, {address: address.value})
    // 确保从响应中正确获取地址值
    if (res && res.address) {
      address.value = res.address
    } else if (res && res.data && res.data.address) {
      // 如果响应数据在data字段中
      address.value = res.data.address
    }
    // 显示成功消息或其他处理
  } catch (error) {
    // 如果更新失败，恢复原来的地址值
    address.value = preAddr.value
    console.error("地址更新失败:", error)
    // 可以添加错误提示
  }
}

const changepwd = () => {
  router.push({
    path: '/user/pwd/',
    query: {
      email: email.value  // 将当前邮箱作为查询参数传递
    }
  })
}

const changeEmail = () => {
  //跳转到邮箱修改页面
  //传递消息

  window.location.href = '/user/email';
}

onMounted(()=>{

})
</script>

<style scoped>
.profile-card {
  max-width: 800px;
  margin: 20px auto;
}

.profile-container {
  display: flex;
  gap: 40px;
  padding: 20px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  border: 3px solid #f0f0f0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.info-item {
  display: flex;
  align-items: baseline;
  font-size: 16px;
}

.info-label {
  width: 100px;
  color: #666;
  font-weight: 500;
}

.info-content {
  flex: 1;
  color: #333;
  font-weight: 600;
  word-break: break-all;
}

.edit-btn {
  width: 120px;
}

.error-message {
  color: #ff4444;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .profile-container {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }

  .info-item {
    flex-direction: column;
    gap: 8px;
  }

  .info-label {
    width: auto;
    font-size: 14px;
  }

  .info-content {
    font-size: 15px;
  }
}
</style>