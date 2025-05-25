

<template>
<h1>我的收藏</h1>
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
        <Product :title="product.title" :price="product.price" :avatar="product.user.avatar" :username="product.user.username" :user_id="product.user.username" :product_id="product.product_id"></Product>
      </el-col>
    </el-row>
    <div v-if="productList.length===0" style="margin: auto">暂无收藏</div>
  </div>
</template>
<script setup>
import Product from "../../components/product.vue";
import {getToken} from "../../utils/user-utils.js";
import {getMyCollections} from "../../api/product/index.js";
import {ref} from "vue";
const productList=ref([]);
const getCollections=async()=>{
  const res=await getMyCollections(getToken()).then(
      res=>{
        console.log(res.results);
        productList.value.push(...res.results.map(item => item.collection))
      }
  );

}
getCollections()
</script>
<style scoped>

</style>