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
          <label class="info-label">手机号：</label>
          <span class="info-content">{{ phone }}</span>
          <el-button @click="changePhone">修改手机号</el-button>
        </div>
        <div class="info-item">
          <label class="info-label">电子邮箱：</label>
          <span class="info-content">{{ email }}</span>
          <el-button @click="changeEmail">修改电子邮箱</el-button>
        </div>
        <el-button style="width: 20%" @click="changepwd">修改密码</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import {useUserStore} from '../../stores/user.js'
import {onMounted, ref,watch} from 'vue'
import {setUserName} from "../../utils/user-utils.js";

let userStore = useUserStore()
const error = ref('')
const emit = defineEmits(['edit'])
const selectedFile = ref(null);
const avatar = ref('')
const nameChanging = ref(false)
const previousName = ref('')
const handleEdit = () => {
  emit('edit')
}
const changeAvatar = (event) => {
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
}
const changeName = () => {
    nameChanging.value=true
  previousName.value=userStore.username
}
const rejectName = () => {
    nameChanging.value=false
  userStore.username=previousName.value
}
const ensureName = () => {
    nameChanging.value=false
    setUserName(userStore.username)
  //
}
const changePhone = () => {
  //跳转到手机号修改页面
  window.location.href = '/user/phone';
}
const changeEmail = () => {
  //跳转到邮箱修改页面
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