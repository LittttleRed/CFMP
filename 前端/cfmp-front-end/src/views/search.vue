<template>
<Head :show-search="true"></Head>
  <el-card class="goods-container" shadow="never">
      <div v-if="loading" class="loading-wrapper">
        <el-icon class="loading-icon" :size="50"><Loading /></el-icon>
      </div>

      <div v-else class="goods-list" style="padding: 10px 10px 0 0">
        <el-row :gutter="10">
        <el-col v-for="(product, index) in productList"
        :key="product.product_id"
        :lg="4"
        :md="8"
        :sm="12"
        :xs="24"
      >
           <Product :title="product.title"
                    :price="product.price"
                    :avatar="product.user.avatar"
                    :username="product.user.username"
                    :user_id="product.user.user_id"
                    :product_id="product.product_id"
                    :media="product.media[0]?product.media[0]['media']:''"
                    :myfollow="myFollow.indexOf(product.user.user_id)!==-1">
           </Product>
          </el-col>
        </el-row>
        <h2 v-if="noProduct" style="margin: auto">暂无此种商品,看看别的吧~</h2>
      </div>
    </el-card>
</template>
<script setup>
import Head from "../components/Head.vue";
import {Loading} from "@element-plus/icons-vue";
import Product from "../components/product.vue";
import {onBeforeRouteLeave, useRoute} from "vue-router";
import {onUnmounted, ref} from "vue";
import {getProducts} from "../api/product/index.js";
import {getAllFollows} from "../api/user/index.js";
import {getToken} from "../utils/user-utils.js";
const route=useRoute()
const keyword=ref(route.query.keyword)
const productList=ref([])
const myFollow=ref([])
const page = ref(1)
const isMax=ref(false)
const loading = ref(true)
const isUpdating = ref(false)
const noProduct = ref(false)
const getUserFollow=async()=> {
 await getAllFollows(getToken()).then(res => {
    myFollow.value=res.map(item => {
      return item.followee
    })
  })
  console.log(myFollow.value)
}
getUserFollow()
const updateProductList=async()=>{
  let page_size=10
  //根据页码获取商品列表
  let data={
    page: page.value,
    page_size: page_size,
  }
  const queryFields = ['keyword', 'category', 'min_price', 'max_price'];

queryFields.forEach(field => {
  if (route.query[field]) {
    data[field] = route.query[field];
  }
});

  console.log(data)
  console.log(data)
   await getProducts(data).then( res => {
     console.log(res["results"])
     if(res["results"].length<page_size){
       productList.value=[...productList.value,...res["results"]]
       isMax.value=true
       console.log("max")
     }else {
       console.log(res["results"])
       productList.value = [...productList.value, ...res["results"]]
     }
      if(productList.value.length===0){
    noProduct.value=true
  }
  })
  loading.value=false
   page.value++

}

updateProductList()
//获取当前可视范围的高度
const getClientHeight=()=> {
    let clientHeight = 0;
    if (document.body.clientHeight && document.documentElement.clientHeight) {
        clientHeight = Math.min(document.body.clientHeight, document.documentElement.clientHeight)
    } else {
        clientHeight = Math.max(document.body.clientHeight, document.documentElement.clientHeight)
    }
    return clientHeight
}
//获取文档完整的高度
const getScrollHeight=()=> {
    return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)
}
//获取当前滚动条的位置
const getScrollTop=()=> {
    let scrollTop = 0;
    //window.pageYOffset = document.documentElement.scrollTop
    if (document.documentElement && document.documentElement.scrollTop) {
        scrollTop = document.documentElement.scrollTop
    } else if (document.body) {
        scrollTop = document.body.scrollTop
    }
    return scrollTop
}
const windowScroll=()=> {
        //获取三个值
        let scrollTop = getScrollTop()
        let clientHeight = getClientHeight()
        let scrollHeight = getScrollHeight()
        //如果满足公式则，确实到底了
        if(scrollTop+clientHeight >= scrollHeight-3&&isUpdating.value===false&&isMax.value===false){
          isUpdating.value=true
          console.log("到底了")
          updateProductList().then(() => {
            isUpdating.value=false
          })
        }
    }

window.addEventListener('scroll', windowScroll,true)
onUnmounted(
    () => {
        window.removeEventListener("scroll",windowScroll);//销毁滚动事件
    },
)
onBeforeRouteLeave(
    (to, from) => {
        window.removeEventListener("scroll",windowScroll);//销毁滚动事件
    },
)
</script>
<style scoped lang="scss">
.goods-container {
    max-width: 1600px;
    margin: 20px auto;

    .loading-wrapper {
      text-align: center;
      padding: 100px 0;

      .loading-icon {
        animation: rotating 2s linear infinite;
      }
    }


  }

</style>