<script setup>
 import Product from '../../components/product.vue'
 import {reactive, ref} from "vue";
 import {getAllMyLaunches} from "../../api/user/index.js";
 import {getToken} from "../../utils/user-utils.js";
let seller = reactive({name: 'seller',})
let title = ref("title")
let productList = ref([])
 productList.value = [

 ]
 const getAllProducts = async () => {
  const res = await getAllMyLaunches(getToken()).then(res => {
     productList.value = res
  })
}
getAllProducts()
</script>

<template>
    <h1>我发布的</h1>
    <div class="product-list">
    <el-row :gutter="10">  <!-- 控制列间距 -->
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
                    :user_id="product.user.username"
                    :product_id="product.product_id"
                    :media="product.media[0]?product.media[0]['media']:''"></Product>
      </el-col>
    </el-row>
  </div>

</template>

<style scoped>

</style>