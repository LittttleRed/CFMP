import axios from 'axios'

const TokenKey = 'vue_admin_template_token'

const http = axios.create({
  baseURL: '/api/',
  timeout: 10000, // 超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

http.interceptors.request.use(config => {
  const token = localStorage.getItem(TokenKey)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  // 添加用户UUID请求头 - 根据后端微服务架构添加
  const userId = localStorage.getItem('user_id')
  if (userId) {
    config.headers['UUID'] = userId         // 保持兼容性
  }

  return config
})

// 响应拦截器
http.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error.response)
    return Promise.reject(error)
  }
)

//
export default http
