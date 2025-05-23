<template>
  <div class="qqmail-login-container">
    <!-- 顶部导航栏 -->
    <div class="login-header">
      <div class="logo-wrapper">
        <span class="logo-text">校园跳蚤市场</span>
      </div>
    </div>

    <!-- 主体登录区域 -->
    <div class="login-main">
      <div class="login-wrapper">
        <!-- 左侧装饰图 -->
        <div class="decorative-image"></div>

        <!-- 右侧登录面板 -->
        <div class="login-panel">
          <div class="panel-header">
            <h2>邮箱密码登录</h2>
          </div>

          <el-form 
            ref="formRef"
            :model="loginForm"
            :rules="rules"
            @submit.prevent="handleLogin"
          >
            <el-form-item prop="email">
              <el-input
                v-model="loginForm.email"
                placeholder="邮箱"
                class="qqmail-input"
                tabindex="1"
              >
                <template #prefix>
                  <span class="input-label">账号</span>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                class="qqmail-input"
                tabindex="2"
                show-password
              >
                <template #prefix>
                  <span class="input-label">密码</span>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item class="remember-item">
              <div class="link-group" style="margin-top: 10px">
                <router-link to="/forgot" class="link">忘记密码？</router-link>
              </div>
            </el-form-item>
            <div class="fail-msg">
              {{fail_msg}}
            </div>
            <el-button
              class="qqmail-login-btn"
              type="primary"
              native-type="submit"
              :loading="loading"
              @click="handleLogin"
            >
              立即登录
            </el-button>
          </el-form>

          <div class="register-section">
            <el-button type="text" class="register-btn">
              还没有账号？<span class="emphasize" @click="router.push('/register')">立即注册</span>
            </el-button>
          </div>
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
import { ref, reactive } from 'vue'
import type { FormInstance } from 'element-plus'
import { useRouter } from 'vue-router'
import { getLogin } from '../api/user'
import {getToken, setToken, setUserId, setUserName} from "../utils/user-utils";
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)
const fail_msg = ref('')
const loginForm = reactive({
  email: '',
  password: ''
})

const rules = {
email: [
  { required: true, message: '邮箱不能为空', trigger: 'blur' },
  {
    pattern: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    message: '请输入有效的邮箱地址',
    trigger: ['blur', 'input'] // 失焦+输入时双重校验
  },
  { max: 254, message: '邮箱长度不能超过254个字符', trigger: 'blur' }
],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 16, message: '长度在6到16个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
   await getLogin(loginForm).then((res) => {
     //如果状态码是404,提示用户未注册
     if (res["success"] === false) {
       fail_msg.value=res["fail_msg"]
     } else {
       console.log(res)
       setToken(res["access_token"])
       setUserId(res["user_id"])
       setUserName(res["username"])
       window.location.href = '/'
     }
})
}
</script>

<style scoped lang="scss">
.fail-msg{
  color: red;
}
.qqmail-login-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f1f6ff;

  .login-header {
    height: 64px;
    background: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    
    .logo-wrapper {
      width: 1200px;
      margin: 0 auto;
      line-height: 64px;
      
      .logo-text {
        font-size: 24px;
        font-weight: bold;
        color: orange;
        letter-spacing: 2px;
      }
    }
  }

  .login-main {
    flex: 1;
    padding: 60px 0;
    
    .login-wrapper {
      width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-around;
      
      .decorative-image {
        width: 600px;
        height: 400px;
        background: url('@/assets/login-bg.png') no-repeat center/contain;
      }

      .login-panel {
        width: 380px;
        background: white;
        border-radius: 8px;
        padding: 40px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);

        .panel-header {
          margin-bottom: 30px;
          h2 {
            color: #333;
            font-size: 20px;
            font-weight: 500;
          }
        }

        .qqmail-input {
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

        .remember-item {
          display: flex;
          justify-content: space-between;
          margin-top: -10px;

          .link-group {
            .link {
              color: #666;
              margin-left: 15px;
              &:hover {
                color: #0066ff;
              }
            }
          }
        }

        .qqmail-login-btn {
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

        .register-section {
          margin-top: 30px;
          text-align: center;
          
          .register-btn {
            color: #666;
            
            .emphasize {
              color: #0066ff;
              font-weight: 500;
              margin-left: 5px;
            }
          }
        }
      }
    }
  }

  .login-footer {
    padding: 20px 0;
    background: white;
    
    .copyright {
      text-align: center;
      color: #999;
      font-size: 12px;
    }
  }
}
</style>