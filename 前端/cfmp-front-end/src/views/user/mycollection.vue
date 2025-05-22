

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
  </div>
</template>
<script setup>
import Product from "../../components/product.vue";
const productList=[];
</script>
<style scoped>

</style>