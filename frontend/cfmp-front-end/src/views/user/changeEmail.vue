<template>
    <el-card class="change-email">
      <el-input class="new-email" type="text" v-model="newemail" placeholder="请输入新邮箱"/>
      <el-button v-if="!hassend" type="primary" @click="sendCap" style="margin-left: 120px">发送验证码</el-button>
      <el-button  type="primary"
                          v-else
                          disabled
                  style="margin-left: 120px"
                        >
                {{ countdown }}
              </el-button>
      <el-input class="new-email" type="text" v-model="captcha" style="margin-top: 40px" placeholder="请输入验证码"/>
      <el-button type="primary" style="margin-top: 40px;margin-left: 120px" @click="ensure">确定</el-button>
      <div style="color: red">{{ fail_msg }}</div>
    </el-card>
</template>

<script setup>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {changeEmail, sendCaptcha} from "@/api/user/index.js";
import {getToken} from "@/utils/user-utils.js";
import {useRoute} from "vue-router";
const newemail = ref('')
const captcha = ref('')
const fail_msg  = ref('')
const hassend = ref(false)
const countdown = ref(60) // 倒计时初始值
const timer = ref(null)   // 用于保存定时器引用
const route = useRoute()
const sendCap= async () => {
  if (newemail.value==='') {
    ElMessage.error('请输入邮箱')
    return
  }
  try {
    hassend.value = true
    countdown.value = 60
    timer.value = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer.value)
        hassend.value = false
      }
    }, 1000)
    await sendCaptcha({scene: 'change_email', email: newemail.value}).catch(
        (e) => {
          fail_msg.value = e.response.data.fail_msg || '验证码发送失败'
        }
    )
  }catch (e){
    fail_msg.value = e.response.data.fail_msg || '验证码发送失败'
  }
    // 启动倒计时

}
const ensure= async () => {
  await changeEmail({new_email: newemail.value, captcha: captcha.value},getToken()).then(
      res => {
        ElMessage.success('修改成功')
        route.push('/user/setting')
      }
  ).catch(error => {
    fail_msg.value = error.response.data.fail_msg
  })
}
</script>

<style scoped>
.change-email{
  max-width: 500px;
  margin: 20px auto;
}
.new-email{
  width: 50%;

}
</style>