<template>
  <RightBar></RightBar>

  <div class="home-container">
    <!-- 顶部导航栏 -->
   <Head :show-search="true"></Head>
    <el-card class="goods-container" style="border-radius: 30px;" shadow="never">
      <div class="home-head" style="border-radius: 30px;margin: 0 auto" >
        <Category style="width: 15%;margin: 0 15px;"></Category>
      <el-card style="width: 30%;margin: 10px;--el-card-border-radius: 20px;" shadow="never">
        <div class="slider-container">
        <div
          class="slider-content"
          :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
            @mouseenter="stopAutoPlay"
            @mouseleave="startAutoPlay"
        >
          <img
            :src="getImageUrl(img)"
            v-for="(img, index) in imageList"
            :key="index"
            class="slider-image"
           alt="商品图片"
            @click="handleClick(index)"
            style="cursor: pointer"/>
        </div>
      </div>
      </el-card>
        <el-card style="width: 45%;margin: 10px;--el-card-border-radius: 20px;" shadow="never">
        <div class="slider-container">
        <div
          class="slider-content"
          :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
            @mouseenter="stopAutoPlay"
            @mouseleave="startAutoPlay"
        >
          <img
            :src="getImageUrl(img)"
            v-for="(img, index) in imageList1"
            :key="index"
            class="slider-image"
           alt="商品图片"/>
        </div>
      </div>
      </el-card>
      </div>
    </el-card>

    <!-- 商品展示区 -->
    <el-card class="goods-container" shadow="never">
      <el-button class="sort_button" @click="sort_type='hot';resort()" v-if="!loading" style="background-color: #ffe63e">最近热门</el-button>
      <el-button class="sort_button" @click="sort_type='score';resort()" v-if="!loading">评分最高</el-button>
      <el-button class="sort_button" @click="sort_type='price'; resort()" v-if="!loading">价格最低</el-button>
      <el-button class="sort_button" @click="sort_type='time';resort()" v-if="!loading">最新发布</el-button>
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
                    :myfollow="myFollow.indexOf(product.user.user_id)!==-1"
                    :functions="product.function"
                    :visit_count="product.visit_count"
                    :status="product.status">
           </Product>
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
import {getToken} from "../utils/user-utils";
import {getAllFollows} from "../api/user"

const productList = ref([])
const loading = ref(true)
const isUpdating = ref(false)
const page = ref(1)
const isMax=ref(false)
const myFollow=ref([])
const imageList=ref([ 'picture_1.png', 'picture_2.png', 'picture_3.png', 'picture_4.png'])
const imageList1=ref([ '制作商品宣传图片.png', '制作商品宣传图片1.png', '制作商品宣传图片2.png', '制作商品宣传图片3.png'])
const currentIndex = ref(0)
let timer = null
const sort_type = ref('')
const chating = ref(true)
const router  = useRouter()
const handleClick = (index) => {
  let category = 0;
  switch (index) {
    case 0:
      category = 3;
      break;
    case 1:
      category = 4;
      break;
    case 2:
      category = 16;
      break;
    case 3:
      category = 19;
      break;
    default:
      return;
  }
  router.push({ name: 'search', query: { category } });
};
const resort = () => {
  page.value = 1;
  isMax.value = false;
  isUpdating.value = false; // 添加这一行确保可再次加载
  productList.value = [];
  loading.value = true;
  updateProductList().then(() => {
    loading.value = false;
  });
}
const getUserFollow=async()=> {
  if(getToken()) {
    await getAllFollows(getToken()).then(res => {
      myFollow.value = res.map(item => {
        return item.followee.user_id
      })
    })
  }
  console.log(myFollow.value)
}
getUserFollow()

onMounted(() => {
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})
const getImageUrl = (name) => {
        return new URL(`../assets/${name}`, import.meta.url).href
    }
const startAutoPlay = () => {
  timer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % imageList.value.length
  }, 5000) // 3秒切换一次
}

const stopAutoPlay = () => {
  clearInterval(timer)
}



const updateProductList = async () => {
  console.log(isUpdating.value)
  console.log(isMax.value)
  if (isUpdating.value || isMax.value) return;

  isUpdating.value = true;

  let page_size = 10;
  let data = {
    page: page.value,
    page_size: page_size,
    status: 0
  };

  if (sort_type.value === 'hot') {
    data["sort_by"] = "1";
  } else if (sort_type.value === 'score') {
    data["sort_by"] = "4";
  } else if (sort_type.value === 'price') {
    data["sort_by"] = "2";
  }

  try {
    const res = await getProducts(data);
    if (res && res.results && res.results.length > 0) {
      console.log(res.results)
      productList.value = [...productList.value, ...res.results];
      if (res.results.length < page_size) {
        isMax.value = true;
      } else {
        isMax.value = false;
      }
    } else {
      isMax.value = true; // 没有更多数据了
    }
  } catch (error) {
    console.error('请求商品列表失败:', error);
    isMax.value = true; // 出错时也停止加载
  } finally {
    loading.value = false;
    isUpdating.value = false;
    page.value++;
  }
};

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
          console.log("到底了")
          updateProductList()
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
.sort_button{
  margin-left: 30px;
  margin-top: 10px;
  height: 50px;
  width: 135px;
  border-radius: 25px;
  font-size: 18px;
  border: none;
  color: black;
  font-weight: bold;
  background-color: #eeeeee;
  &:hover{
    background-color: #ffe63e;
  }
}
.slider-container {
  width: 100%;
  height: 40vh;/* 根据需求调整高度 */
  overflow: hidden;
  position: relative;
}

.slider-content {
  display: flex;
  height: 100%;
  transition: transform 0.5s ease-in-out; /* 取消过渡效果实现立即切换 */
}

.slider-image {
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片比例填充容器 */
  border-radius: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.home-head  {
  display: flex;
  align-items: center;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  z-index: 1000;
  max-width: 1600px;
  margin: 20px auto;
}
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