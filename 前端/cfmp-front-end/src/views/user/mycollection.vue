<template>
<h1>我的收藏</h1>
  <div class="product-list" v-loading="loading">
    <el-row :gutter="10">  <!-- 控制列间距 -->
      <el-col
        v-for="(product, index) in productList"
        :key="index"
        :lg="4"
        :md="8"
        :sm="12"
        :xs="24"
      >
        <Product 
          :title="product.title" 
          :price="product.price" 
          :avatar="product.user_info?.avatar || ''" 
          :username="product.user_info?.username || ''" 
          :user_id="product.user_info?.user_id || ''" 
          :product_id="product.product_id" 
          :media="product.media && product.media[0] ? product.media[0].media : null">
        </Product>
      </el-col>
    </el-row>
    <div v-if="!loading && productList.length===0" style="margin: auto">暂无收藏</div>
  </div>
</template>
<script setup>
import Product from "../../components/product.vue";
import {getToken} from "../../utils/user-utils.js";
import {getMyCollections} from "../../api/product/index.js";
import {ref} from "vue";
const productList=ref([]);
const loading = ref(true);
const getCollections=async()=>{
  try {
    loading.value = true;
    const res=await getMyCollections(getToken());
    console.log("收藏列表响应:", res);
    // 正确处理收藏数据，从collection字段中提取商品信息
    productList.value = res.results.map(item => {
      // 后端返回的数据结构是 {collection: {...商品信息...}, collecter: {...收藏者信息...}}
      // 我们需要的是商品信息，它在collection字段中
      return item.collection || {};
    });
  } catch (error) {
    console.error("获取收藏列表失败:", error);
    productList.value = []; // 出错时清空列表
  } finally {
    loading.value = false;
  }
}
getCollections()
</script>
<style scoped>

</style>