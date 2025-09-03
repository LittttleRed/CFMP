import http from "../../utils/request.js";

export const getAllUser=(params)=>{
    return http({
        url:'root/user/',
        method:'get',
         params:params,
        headers: {
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        },
    })
}
export const getUserByID=(id)=>{
    return http({
        url:'root/user/'+id,
        method:'get',
    })
}

export const changeUserState=(id,status)=>{
    return http({
        url:'root/user/'+id+'/',
        method:'patch',
        data:{
            status:status
        }
    })
}
export const getAllComplaints=(target_type,params)=>{
    return http(
        {
            url:'complaints/',
            method:'get',
            params:{
                target_type:target_type,
                ...params
            }
        }
    )
}
export const getComplaintByID=(id)=>{
    return http({
        url:'complaints/'+id+'/',
        method:'get',
    })
}
export const createReview=(data)=>{
    return http({
        url:'reviews/',
        method:'post',
        data:data
    })
}
export const updateReview=(id,type,status)=>{
    return http({
        url:'complaints/branch/'+type+'/'+id+'/',
        method:'patch',
        data:{
            status:status
        }
    })
}

export const getOrders=(day,status)=>{
    return http({
        url:'root/order/',
        method:'get',
        params:{
            day:day,
            status:status
        }
    })
}
import request from "@/utils/request";

// 获取所有商品
export function getAllProducts(params) {
  return request({
    url: "/root/products/",
    method: "get",
    params
  });
}

// 根据 ID 获取商品
export function getProductById(id) {
  return request({
    url: `/root/products/${id}/`,
    method: "get"
  });
}

// 更新商品状态
export function updateProductStatus(productId, status) {
  return request({
    url: `/root/products/${productId}/`,
    method: "patch",
    data: { status }
  });
}
