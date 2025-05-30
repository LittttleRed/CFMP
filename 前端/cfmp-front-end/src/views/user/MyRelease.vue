<script setup>
 import Product from '../../components/product.vue'
 import {reactive, ref} from "vue";
 import {getAllLaunches} from "../../api/user/index.js";
 import {getToken, getUserId} from "../../utils/user-utils.js";
 import {useRoute, useRouter} from "vue-router";
let seller = reactive({name: 'seller',})
let title = ref("title")
let productList = ref([])
 productList.value = [

 ]
 const router = useRouter()
 const route = useRoute()
 const getAllProducts = async () => {
  if(!getToken()){
    return
  }
  if(route.query.user_id === getUserId() || route.query.user_id === undefined){
  const res = await getAllLaunches(getToken(),getUserId()).then(res => {
     productList.value = res
  })
  }else{
  const res = await getAllLaunches(getToken(),route.query.user_id).then(res => {
     productList.value = res
  })
  }
}
getAllProducts()
</script>

<template>
    <h1>我发布的</h1>
    <div class="product-list">
    <el-row :gutter="10" v-if="getToken()">  <!-- 控制列间距 -->
      <el-col
        v-for="(product, index) in productList"
        :key="index"
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
                    :status="product.status"></Product>
      </el-col>
    </el-row>
      <div v-else>
        <p>登录后可查看</p>
      </div>
  </div>

</template>

<style scoped>

</style>