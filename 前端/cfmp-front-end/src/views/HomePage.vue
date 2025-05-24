<template>
  <RightBar></RightBar>
  <div class="home-container">
    <!-- 顶部导航栏 -->
   <Head :show-search="true"></Head>

    <Category style="width: 60%;margin: 10px auto"></Category>
    <!-- 商品展示区 -->
    <el-card class="goods-container" shadow="never">
      <div v-if="loading" class="loading-wrapper">
        <el-icon class="loading-icon" :size="50"><Loading /></el-icon>
      </div>

      <div v-else class="goods-list">
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
                    :user_id="product.user.username"
                    :product_id="product.product_id"
                    :media="product.media[0]?product.media[0]['media']:''"></Product>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 分页器 -->
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, provide, onUnmounted} from 'vue'
import { Search, Loading } from '@element-plus/icons-vue'
import {onBeforeRouteLeave, useRouter} from 'vue-router'
import { useUserStore } from '../stores/user.js'
import GoodsItem from '../components/GoodsItem.vue'
import Product from "../components/product.vue";
import Head from "../components/Head.vue";
import Category from "../components/home/category.vue";
import RightBar from "./RightBar.vue";
import {getProducts} from "../api/product";

const productList = ref([])
const loading = ref(true)
const isUpdating = ref(false)
const page = ref(1)
const isMax=ref(false)
const updateProductList=async()=>{
  let page_size=10
  //根据页码获取商品列表
  let data={
    page: page.value,
    page_size: page_size
  }
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
.home-container {
  min-height: 100vh;
  background-color: #f5f7fa;

  .nav-bar {
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    background: white;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    z-index: 1000;

    .nav-left {
      display: flex;
      align-items: center;
      gap: 30px;
      width: 1200px;
      margin: 0 auto;

      .logo {
        font-size: 24px;
        font-weight: bold;
        color: #0066ff;
      }

      .search-input {
        width: 400px;
      }
    }
     .nav-right {
    padding-left: 4px;
     min-width: 300px; // 与左侧保持间距
  }


  }

  .goods-container {
    max-width: 1500px;
    margin: 20px auto;

    .loading-wrapper {
      text-align: center;
      padding: 100px 0;

      .loading-icon {
        animation: rotating 2s linear infinite;
      }
    }


  }

  .pagination-wrapper {
    padding: 20px;
    display: flex;
    justify-content: center;
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>