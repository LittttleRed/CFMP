<script setup>
 import Product from '../../components/product.vue'
 import {reactive, ref, onUnmounted, nextTick} from "vue";
 import {getAllLaunches} from "../../api/user/index.js";
 import {getToken, getUserId} from "../../utils/user-utils.js";
 import {useRoute, useRouter} from "vue-router";

let seller = reactive({name: 'seller',})
let title = ref("title")
let productList = ref([])
let isLoading = ref(false)
let isMounted = ref(true)

 productList.value = [

 ]
 const statusMap = {
  'on-sale': 0,     // 在售
  'had-sale': 2,    // 已售出
  'on-sure': 3,     // 未审核
  'on-fail': 1      // 被封禁
}

// 添加当前激活标签
const activeTab = ref('on-sale')

// 添加标题映射
const tabTitles = {
  'on-sale': '在售商品',
  'had-sale': '已售出商品',
  'on-sure': '未审核商品',
  'on-fail': '被封禁商品'
}
const isMyHome = ref(false)
 const router = useRouter()
 const route = useRoute()
const getAllProducts = async () => {
  if(!getToken() || !isMounted.value) return

  isLoading.value = true

  try {
    // 获取当前状态码
    const status = statusMap[activeTab.value]

    if(route.query.user_id === getUserId() || route.query.user_id === undefined) {
      const res = await getAllLaunches(getToken(), getUserId(), status)
      if(isMounted.value) {
        productList.value = res || []
        isMyHome.value = true
      }
    } else {
      const res = await getAllLaunches(getToken(), route.query.user_id, status)
      if(isMounted.value) {
        productList.value = res || []
      }
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
    if(isMounted.value) {
      productList.value = []
    }
  } finally {
    if(isMounted.value) {
      isLoading.value = false
    }
  }
}

getAllProducts()

const handleTabChange=(name)=>{
  if(!isMounted.value) return
  productList.value=[]
  activeTab.value=name
  console.log(name)
  getAllProducts()
}

onUnmounted(() => {
  isMounted.value = false
})
</script>

<template>
    <h1 style="margin-left: 60px">{{ isMyHome ? '我发布的' : 'TA发布的' }}</h1>

  <el-tabs v-model="activeTab" @tab-change="handleTabChange">
            <el-tab-pane label="在售" name="on-sale"></el-tab-pane>
            <el-tab-pane label="已售出" name="had-sale"></el-tab-pane>
            <el-tab-pane label="未审核" name="on-sure" v-if="isMyHome"></el-tab-pane>
            <el-tab-pane label="被封禁" name="on-fail" v-if="isMyHome"></el-tab-pane>
          </el-tabs>
    <div class="product-list" v-loading="isLoading">
      <h2 v-if="productList.length===0 && !isLoading" style="margin: auto">暂无</h2>
    <el-row :gutter="10" v-if="getToken()">  <!-- 控制列间距 -->
      <el-col
        v-for="(product, index) in productList"
        :key="product.product_id || index"
        :lg="4"
        :md="8"
        :sm="12"
        :xs="24"
      >
        <Product v-if="product && product.user"
                    :title="product.title"
                    :price="product.price"
                    :avatar="product.user?.avatar || ''"
                    :username="product.user?.username || ''"
                    :user_id="product.user?.user_id || ''"
                    :product_id="product.product_id"
                    :media="product.media && product.media[0] ? product.media[0]['media'] : ''"
                    :status="product.status"></Product>
      </el-col>
    </el-row>
      <div v-else>
        <p>登录后可查看</p>
      </div>
  </div>

</template>

<style scoped>
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
.product-list{
  margin-top: 20px;
}
</style>