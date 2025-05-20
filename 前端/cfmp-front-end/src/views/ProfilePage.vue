<template>
  <div class="profile-container">
    <!-- 头部标题 -->
    <div class="header">
         <el-button 
        type="text" 
        class="back-btn" 
        @click="goBack"
      >
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>个人中心</h1>
    </div>

    <!-- 主体内容 -->
    <div class="content-wrapper">
      <!-- 左侧头像区 -->
      <div class="avatar-section">
        <el-upload
          class="avatar-uploader"
          action="/api/upload"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="userStore.avatar" :src="userStore.avatar" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
        <p class="upload-tip">点击修改头像</p>
      </div>

      <!-- 右侧表单区 -->
      <div class="form-section">
        <el-form 
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-width="100px"
        >
          <!-- 不可编辑字段 -->
          <el-form-item label="账号" prop="username">
            <el-input v-model="userStore.username" disabled />
          </el-form-item>

          <!-- 可编辑字段 -->
          <el-form-item label="联系方式" prop="phone">
            <el-input v-model="formData.phone" placeholder="请输入手机号" />
          </el-form-item>

          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="formData.email" placeholder="请输入邮箱" />
          </el-form-item>

          <el-form-item label="所在校区" prop="campus">
            <el-select v-model="formData.campus" placeholder="请选择校区">
              <el-option
                v-for="item in campusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="详细地址" prop="address">
            <el-input
              v-model="formData.address"
              type="textarea"
              :rows="3"
              placeholder="例如：XX宿舍楼XX房间"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm">保存修改</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import type { UploadProps } from 'element-plus'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const formRef = ref()

// 表单数据
const formData = reactive({
  phone: '',
  email: '',
  campus: '',
  address: ''
})

// 校区选项
const campusOptions = [
  { value: 'north', label: '北校区' },
  { value: 'south', label: '南校区' },
  { value: 'east', label: '东校区' }
]

// 验证规则
const rules = {
  phone: [
    { required: true, message: '请输入联系方式', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  campus: [
    { required: true, message: '请选择校区', trigger: 'change' }
  ]
}

// 初始化加载数据
onMounted(() => {
  loadUserData()
})

// 加载用户数据
const loadUserData = () => {
  // 模拟从API获取数据
  Object.assign(formData, {
    phone: '13800138000',
    email: 'user@campus.com',
    campus: 'north',
    address: '北校区3号宿舍楼201室'
  })
}

// 头像上传处理
const handleAvatarSuccess: UploadProps['onSuccess'] = (response) => {
  userStore.avatar = URL.createObjectURL(response.raw)
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('头像必须为JPG/PNG格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过2MB!')
    return false
  }
  return true
}

// 提交表单
const submitForm = async () => {
  try {
    await formRef.value.validate()
    
    // 调用更新接口
    // await userStore.updateProfile(formData)
    
    ElMessage.success('个人信息更新成功')
  } catch (error) {
    console.error('保存失败', error)
  }
}

// 重置表单
const resetForm = () => {
  formRef.value.resetFields()
  loadUserData()
}
const goBack = () => {
  router.back() // 返回上一页
  // 或指定路径 router.push('/home')
}
</script>

<style scoped lang="scss">
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;

  .header {
    margin-bottom: 40px;
    text-align: center;
    h1 {
      font-size: 28px;
      color: #303133;
    }
  }

  .content-wrapper {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: 60px;

    .avatar-section {
      text-align: center;
      
      .avatar-uploader {
        margin: 0 auto 20px;
        width: 160px;
        height: 160px;
        border-radius: 50%;
        overflow: hidden;
        border: 2px dashed #dcdfe6;
        transition: border-color 0.3s;

        &:hover {
          border-color: #409eff;
        }

        .avatar {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        :deep(.el-upload) {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .avatar-uploader-icon {
          font-size: 28px;
          color: #8c939d;
        }
      }

      .upload-tip {
        color: #909399;
        font-size: 14px;
      }
    }

    .form-section {
      padding-right: 60px;

      :deep(.el-form-item__label) {
        font-weight: 500;
      }

      .el-input, .el-select {
        width: 100%;
        max-width: 400px;
      }

      .el-textarea {
        max-width: 600px;
      }
    }
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    grid-template-columns: 1fr;
    
    .avatar-section {
      margin-bottom: 30px;
    }

    .form-section {
      padding-right: 0;
    }
  }
}
</style>