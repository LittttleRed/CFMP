const TokenKey = 'vue_admin_template_token'

export function getToken() {
  return localStorage.getItem(TokenKey)
}

export function setToken(token: string) {
  localStorage.setItem(TokenKey, token)
}

export function removeToken() {
  localStorage.removeItem(TokenKey)
}

export function getUserName() {
  return localStorage.getItem('userName')
}
export function setUserName(userName: string) {
  localStorage.setItem('userName', userName)
}

export function removeUserName() {
  localStorage.removeItem('userName')
}

export function getUserId() {
  return localStorage.getItem('user_id')
}
export function setUserId(userId: string) {
  localStorage.setItem('user_id', userId)
}
export function removeUserId() {
  localStorage.removeItem('user_id')
}
//头像
export function getHeadImg() {
  return localStorage.getItem('headImg')
}
export function setHeadImg(headImg: string) {
  localStorage.setItem('headImg', headImg)
}
export function removeHeadImg() {
  localStorage.removeItem('headImg')
}
export function setStaff(staff: string) {
  localStorage.setItem('staff', staff)
}
export function removeStaff() {}
export function getStaff(){
  return localStorage.getItem('staff')
}
