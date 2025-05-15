import axios from 'axios'
const http = axios.create({
  baseURL: '/api/',
  timeout: 10000, // 超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})
http.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
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

export default http