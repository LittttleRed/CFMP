import { defineStore } from 'pinia';
import {getToken,setToken,removeToken} from "../utils/user-utils.js";
export const UserInfoStore = defineStore('userInfo', {

	state: () => ({
    token: getToken(),
    username: getUserName(),
    user_id: getUserId(),
    headImg: getHeadImg(),
  }),

	actions: {
    // 登陆的异步action
    async login (loginForm) {
       // 发送登陆的请求
      const result = await getLogin(loginForm)
      // 请求成功后, 取出token保存  pinia和local中
      const token = result.token

      this.token = token
      setToken(token)
    },
    async getInfo () {
      // const result = await getUserInfo()
      // this.nickName = result.loginUser.nickName
      // this.uid = result.loginUser.uid
      // setUserName()
      // setUserId()
      // setHeadImg()
    },
    initUserInfo(){
      removeToken()
      removeUserName()
      removeUserId()
      removeHeadImg()
      console.log('1111111111');
    }

  },


});