<template>
  <div class="mail-login-container">
    <!-- 动态背景容器（粒子效果） -->
    <ParticlesComponent
      id="tsparticles"
      class="login__particles"
      :options="particles_config"
      :particlesInit="particlesInit"
    />
    <!-- 顶部导航栏 -->
     
    <div class="login-header" style="z-index: 1;">
      <div class="logo-wrapper">
        <img 
          src="../assets/logo1.png"
          alt="校园跳蚤市场"
          class="logo-image"
        />
        <span class="logo-text">校园跳蚤市场</span>
      </div>
    </div>

    <!-- 主体登录区域 -->
    <div class="login-main" style="z-index: 1;">
      <div class="login-wrapper">
        <!-- 左侧装饰图 -->
        <div class="decorative-image"></div>

        <!-- 右侧登录面板 -->
        <div class="login-panel">
          <div class="panel-header">
            
              <div class="back-button-container">
                <el-button
                  type="text"
                  @click="handleBack"
                  class="back-button"
                  >
                  <el-icon :size="24" class="arrow-icon">
                    <ArrowLeft />
                  </el-icon>
                  <span class="back-text">返回</span>
                </el-button>
              </div>

              <h2>注册账号
                 <span class ="switch-type">
              <router-link
                to="/register/email"
                class="switch-link"
                :class="{ 'active': $route.path === '/register/email' }"
                >邮箱注册
              </router-link>
               <span class="divider">|</span>
               <router-link
                 to="/register/phone"
                 class="switch-link"
                 :class="{ 'active': $route.path === '/register/phone' }"
               >
                 手机号注册
               </router-link>
            </span>
              </h2>
           
          </div>

          <el-form
            ref="formRef"
            :model="registerForm"
            :rules="rules"
            @submit.prevent="handleRegister"
          >
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名"
                class="mail-input"
                tabindex="1"
              >
                <template #prefix>
                  <span class="input-label">用户名</span>
                </template>

              </el-input>
            </el-form-item>

            <el-form-item prop="message">
              <el-input
                v-model="registerForm.message"
                :placeholder="SelectWays"
                class="mail-input"
                tabindex="1"
              >
                <template #prefix>
                  <span class="input-label">账号</span>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码"
                class="mail-input"
                tabindex="2"
                show-password
              >
                <template #prefix>
                  <span class="input-label">密码</span>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="password_repeat">
              <el-input
                v-model="registerForm.password_repeat"
                type="password"
                placeholder="重复密码"
                class="mail-input"
                tabindex="2"
                show-password
              >
                <template #prefix>
                  <span class="input-label" style="margin-right: 30px">重复密码</span>
                </template>
              </el-input>
            </el-form-item>

            <el-button
              class="mail-login-btn"
              type="primary"
              native-type="submit"
              :loading="loading"
            >
              注册
            </el-button>
          </el-form>
        </div>
      </div>
    </div>

    <!-- 底部版权信息 -->
    <div class="login-footer">
      <p class="copyright">© CampusMarket 校园交易平台</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { FormInstance } from 'element-plus'
import { useRouter } from 'vue-router'
import { getRegister } from '../api/user'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ParticlesComponent } from 'particles.vue3';
import { loadSlim } from 'tsparticles-slim'
import { particles_config } from '../components/background/particles-config'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)

const registerForm = reactive({
  username: '',
  password: '',
  password_repeat: '',
  message: '',
  captcha: ''
})

const particlesInit = async engine => {
    //await loadFull(engine);
    await loadSlim(engine);
};

const rules = {
  username: [
    { required: true, message: '账号不能为空', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在6到20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 16, message: '长度在6到16个字符', trigger: 'blur' }
  ],
  repeatPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule: any, values: string, callback: any)=>{
        if (values !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
        trigger: ['blur', 'input']
      }
    }
  ]
}

const handleRegister = async () => {
  try{
    loading
    await formRef.value?.validate()
    const res = await getRegister(registerForm)

    if (res.status === 200){
      console.log('注册成功')
      router.push('/login')
  }else{
      console.error('注册失败', res.data)
      loading.value = false
  }
  }catch (error) {
    // 处理验证失败的情况  res.status === 400 or others
  }finally {
    loading.value = false
  }
}
const handleBack = () => {
  router.push('/login')
}
const SelectWays = computed (() =>{
  if(router.currentRoute.value.path === '/register/email') {
    return 'email'
  } else if (router.currentRoute.value.path === '/register/phone') {
    return 'phone'
  }
  return '未知'
})


</script>

<style scoped lang="scss">
.login__particles {
  position: fixed;
  left: 0; top: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none; // 避免遮挡表单交互
}
.back-button-container{
  position: relative;
  margin-bottom: 0px;
}
.back-button {
  padding: 0;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  &:hover{
    transform: translateX(-5px);
    .arrow-icon{
      color: var(--el-color-primary);
    }
    .back-text{
      color: var(--el-color-primary);
    }
  }
}
.arrow-icon{
  transition: color 0.3s ease;
  color: #666;
}
.back-text{
  margin-left: 8px;
  font-size: 16px;
  transition: color 0.3s ease;
  color: #666;
}
.login__particles {
  position: fixed;
  left: 0; top: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
}
.mail-login-container  {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  position: relative;
}
.login-header {
  height: 100px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  .logo-wrapper {
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 20px;
    .logo-text {
      font-size: 24px;
      font-weight: bold;
      color: orange;
      letter-spacing: 2px;
      margin-left:10px;
    }
    .logo-image {
      width: 100px;
      height: 100%;
      display: block;
      object-fit: contain;
    }
  }
}
.login-main {
  flex: 1;
  padding: 60px 0;
  .login-wrapper {
    width: 100%;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center; // 居中
    // .decorative-image { ... } // 如需保留可自定义
    .login-panel {
       margin-left:  calc(80% - 380px);
        margin-right: auto ;
        width: 380px;
        background: white;
        border-radius: 8px;
        padding: 40px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        background: rgba(255, 255, 255, 0.92); // 增加透明度
        backdrop-filter: blur(8px); // 添加毛玻璃效果
        border: 1px solid rgba(255, 255, 255, 0.2); // 增加边框

      .panel-header {
        margin-bottom: 30px;
        h2 {
          color: #333;
          font-size: 20px;
          font-weight: 500;
        }
      }
      .mail-input {
        :deep(.el-input__wrapper) {
          height: 48px;
          padding: 0 15px;
          border-radius: 4px;
          box-shadow: 0 0 0 1px #dcdfe6;
          &.is-focus {
            box-shadow: 0 0 0 1px #0066ff !important;
          }
        }
        .input-label {
          color: #606266;
          margin-right: 12px;
          width: 40px;
          display: inline-block;
        }
      }
      .mail-login-btn {
        width: 100%;
        height: 48px;
        font-size: 16px;
        background: #0066ff;
        border: none;
        margin-top: 20px;
        &:hover {
          opacity: 0.9;
        }
      }
    }
  }
}
.login-footer {
  padding: 20px 0;
  background: white;
  z-index: 1;
  .copyright {
    text-align: center;
    color: #999;
    font-size: 12px;
  }
}
</style>