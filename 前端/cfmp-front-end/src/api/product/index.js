import http from "../../utils/request.js";

export const getAllCategory=()=>{
    return http({
        url:'/product/category/',
        method:'get',
    })
}
export const getProducts=(data)=>{
    return http({
        url:'/product/',
        method:'get',
        params:data,
    })

}

export const addProduct=(data,token)=>{
    return http({
        url:'/product/',
        method:'post',
        data:data,
        headers:{
            'Authorization':'Bearer '+token,
            'Content-Type':'multipart/form-data'
        }
    })
}
export const getProduct=(id)=>{
    return http({
        url:'/product/'+id,
        method:'get',
    })
}
