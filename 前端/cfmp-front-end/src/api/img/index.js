import http from '../../utils/request.js'
export const uploadFile=(data)=>{
    return http({
        url:'/v1/test_img/',
        method:'post',
        data:data,
        headers:{
            'Content-Type':'multipart/form-data'
        }
    })
}
export const getFile=(data)=>{
    return http({
        url:'/v1/test_img/',
        method:'get',
        params:data,
        headers:{
            'Content-Type':'multipart/form-data'
        }
    })
}