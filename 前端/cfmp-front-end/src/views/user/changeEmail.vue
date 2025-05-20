<template>
    <el-card class="change-email">
      <el-input class="new-email" type="text" v-model="newemail" placeholder="请输入邮箱"/>
      <el-button type="primary" @click="sendCaptcha" style="margin-left: 120px">发送验证码</el-button>
      <el-input class="new-email" type="text" v-model="captcha" style="margin-top: 40px" placeholder="请输入验证码"/>
      <el-button type="primary" style="margin-top: 40px;margin-left: 120px" @click="ensureCaptcha">确定</el-button>
    </el-card>
</template>

<script setup>
import {ref} from "vue";
const newemail = ref('')
const captcha = ref('')
const sendCaptcha= ()=>{

}
const ensureCaptcha= ()=>{

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