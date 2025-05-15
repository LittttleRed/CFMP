import http from "../../utils/request.js";

export const getAllUser=()=>{
    return http({
        url:'root/user/',
        method:'get',
         params:{
             page:1,
         }
    })
}