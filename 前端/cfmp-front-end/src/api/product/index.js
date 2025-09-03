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
        url:'/product/'+id+'/',
        method:'get',
    })
}
export const updateProduct=(id,data,token)=>{
    return http({
        url:'/product/'+id+'/',
        method:'put',
        data:data,
        headers:{
            'Authorization':'Bearer '+token,
            'Content-Type':'multipart/form-data'
        }
    })
}
export const getMyCollections=(token)=>{
    return http({
        url:'/product/collections/',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const checkCollection=(id,token)=>{
    return http({
        url:'/product/'+id+'/collection',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const addCollection=(id,token)=>{
    return http({
        url:'/product/'+id+'/collection/',
        method:'post',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const removeCollection=(id,token)=>{
    return http({
        url:'/product/'+id+'/collection/',
        method:'delete',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const updateImg=(id,data,token)=>{
    return http({
        url:'/product/'+id+'/media/bulk/',
        method:'put',
        data:data,
        headers:{
            'Authorization':'Bearer '+token,
            'Content-Type':'multipart/form-data'
        }
    })
}
export const getAllImage=(id,token)=>{
    return http({
        url:'/product/'+id+'/media/',
        method:'get',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const deletePro=(id,token)=>{
    return http({
        url:'/product/'+id+'/',
        method:'delete',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const getProductReviews=(id)=>{
    return http({
        url:'/product/'+id+'/reviews/',
        method:'get',
    })
}
export const addReview=(id,data,token)=>{
    return http({
        url:'/product/'+id+'/reviews/',
        method:'post',
        data:data,
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}
export const deleteReview=(productId, reviewId, token)=>{
    return http({
        url:'/product/'+productId+'/reviews/'+reviewId+'/',
        method:'delete',
        headers:{
            'Authorization':'Bearer '+token,
        }
    })
}