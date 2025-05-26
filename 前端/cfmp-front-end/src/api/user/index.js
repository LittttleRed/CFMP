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
export const sendCaptcha=(data)=>{
    return http({
        url:'/v1/captcha/',
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
        url:'/v1/user/info/',
        method:'get',
        headers:{
            'Authorization':token
        }
    })
}
export const updateUserName=(token,name)=>{
    return http({
        url:'/v1/user/username/',
        method:'patch',
        headers:{
            'Authorization':token
        },
        data: {
            'new_username':name
        }
    })
}
export const getUserById=(id)=>{
    return http({
        url:'/v1/user/'+id,
        method:'get',
    })
}
export const updateAvatar=(token,avatar)=>{
    return http({
        url:'/v1/user/avatar/',
        method:'post',
        headers:{
            'Authorization':'Bearer '+token,
            'Content-Type':'multipart/form-data'
        },
        data: {
            'avatar':avatar
        }
    })
}
export const getMe=(token)=>{
    return http({
        url:'/v1/user/me/',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token
        }
    })
}
export const changeUser=(token,data)=>{
    return http({
        url:'/v1/user/me/',
        method:'patch',
        headers:{
            'Authorization':'Bearer '+token
        },
        data:data
    })
}
export const getAllLaunches=(token,id)=>{
    return http({
        url:'/v1/user/me/products/'+id+'/',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token
        }
    })
}
export const createComplaint=(token,data)=>{
    return http({
        url:'/v1/user/complaint/',
        method:'post',
        headers:{
            'Authorization':'Bearer '+token
        },
        data:data
    })
}
export const followUser=(token,id)=>{
    return http({
        url:'/v1/user/follow/'+id+'/',
        method:'post',
        headers:{
            'Authorization':'Bearer '+token
        }
    })
}
export const unfollowUser=(token,id)=>{
    return http({
        url:'/v1/user/follow/'+id+'/',
        method:'delete',
        headers:{
            'Authorization':'Bearer '+token
        }
    })
}
export const getAllFollows=(token)=>{
    return http({
        url:'/v1/user/follow/',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token
        }
    })
}
export const getAllFollowees=(token)=>{
    return http({
        url:'/v1/user/followee/',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token
        }
    })
}