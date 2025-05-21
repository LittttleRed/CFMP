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