import http from "../../utils/request.js";

export const getLogin=(data)=>{
    return http({
        url:'/v1/auth/login-with-password/',
        method:'post',
        data:data,
    })
}
export const getRegister=(data)=>{
    return http({
        url:'/v1/auth/register/',
        method:'post',
        data:data,
    })
}
export const loginWithCaptcha=(data)=>{
    return http({
        url:'/v1/auth/login-with-captcha/',
        method:'post',
        data:data,
    })
}
export const getUserInfo=(token)=>{
    return http({
        url:'/v1/user/info',
        method:'get',
        headers:{
            'Authorization':token
        }
    })
}
export const updateUserName=(token,name)=>{
    return http({
        url:'/v1/user/username',
        method:'patch',
        headers:{
            'Authorization':token
        },
        data: {
            'new_username':name
        }
    })
}