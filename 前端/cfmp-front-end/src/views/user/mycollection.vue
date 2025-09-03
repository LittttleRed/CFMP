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
          :avatar="product.user?.avatar || ''" 
          :username="product.user?.username || ''" 
          :user_id="product.user?.user_id || ''" 
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
    console.log(res.results);
    productList.value.push(...res.results.map(item => item.collection))
  } catch (error) {
    console.error("获取收藏列表失败:", error);
  } finally {
    loading.value = false;
  }
}
getCollections()
</script>
<style scoped>

</style>