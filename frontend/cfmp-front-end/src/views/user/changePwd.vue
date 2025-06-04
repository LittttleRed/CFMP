<template>
  <el-card class="change-pwd">
    <h2>修改密码</h2>

    <el-input
      v-model="newPassword"
      type="password"
      placeholder="请输入新密码"
      show-password
      class="input-field"
    />

    <el-input
      v-model="confirmPassword"
      type="password"
      placeholder="请确认新密码"
      show-password
      class="input-field"
    />

    <el-button
      v-if="!hassend"
      type="primary"
      @click="sendVerificationCode"
      style="margin-left: 75%"
    >
      发送验证码
    </el-button>

    <el-button
      v-else
      type="primary"
      disabled      style="margin-left: 75%"
    >
      {{ countdown }} 秒后重发
    </el-button>

    <el-input
      v-model="captcha"
      type="text"
      placeholder="请输入验证码"
      class="input-field"      style="margin-top: 20px"
    />

    <el-button
      type="primary"
      @click="submitChange"      style="margin-top: 10px; margin-left: 75%"
    >
      确定
    </el-button>

    <div style="color: red; margin-top: 10px">{{ fail_msg }}</div>
  </el-card>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'
import { sendCaptcha, changePassword } from '@/api/user/index.js'
import {getToken} from '@/utils/user-utils.js'
import {useRoute, useRouter} from 'vue-router'

const route = useRoute()
const router = useRouter()

// 接收通过路由传递的 email
const email = ref(route.query.email || '')  // ✅ 接收到的邮箱地址

const newPassword = ref('')
const confirmPassword = ref('')
const captcha = ref('')
const fail_msg = ref('')
const hassend = ref(false)
const countdown = ref(60)
const timer = ref(null)

// ✅ 发送验证码（使用传入的 email）
const sendVerificationCode = async () => {
  if (!email.value) {
    ElMessage.error('邮箱信息异常')
    return
  }

  try {
    if(newPassword.value!==confirmPassword.value){
      ElMessage.error('两次输入的密码不一致')
      return
    }
    startCountdown()
    await sendCaptcha({scene: 'change_password', email: email.value})
    ElMessage.success('验证码已发送')
  } catch (error) {
    fail_msg.value = error.response?.data?.fail_msg || '验证码发送失败'
  }
}

// ✅ 开始倒计时
const startCountdown = () => {
  hassend.value = true
    countdown.value = 60
    timer.value = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer.value)
        hassend.value = false
      }
    }, 1000)
}


// ✅ 提交修改密码
const submitChange = async () => {
  if (!newPassword.value || !confirmPassword.value || !captcha.value) {
    ElMessage.warning('请填写所有字段')
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  if (!email.value) {
    ElMessage.error('邮箱信息异常，请返回重试')
    return
  }

  try {
    await changePassword({
      new_password: newPassword.value,
      captcha: captcha.value,
      new_password_repeat: confirmPassword.value,
    }, getToken())

    ElMessage.success('密码修改成功')
    newPassword.value = ''
    confirmPassword.value = ''
    captcha.value = ''
    fail_msg.value = ''
  } catch (error) {
    fail_msg.value = error.response?.data?.fail_msg || '修改失败，请重试'
  }
}
</script>

<style scoped>
.change-pwd {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.input-field {
  width: 100%;
  margin-bottom: 20px;
}
</style>