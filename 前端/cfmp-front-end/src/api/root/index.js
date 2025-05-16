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
            url:'root/complaint/',
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
        url:'root/complaint/'+id+'/',
        method:'get',
    })
}
export const createReview=(data)=>{
    return http({
        url:'root/review/',
        method:'post',
        data:data
    })
}
export const updateReview=(id,type,status)=>{
    return http({
        url:'root/complaint/branch/'+type+'/'+id+'/',
        method:'patch',
        data:{
            status:status
        }
    })
}