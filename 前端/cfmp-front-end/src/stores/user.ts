import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '用户昵称',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    phone: '',
    email: '',
    campus: '',
    address: ''
  }),
  actions: {
    logout() {
      // 清除用户信息逻辑
    },
     async updateProfile(data: Record<string, any>) {
      // 调用更新接口
      Object.assign(this, data)
    }
  }
})