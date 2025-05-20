<script setup>
 import Product from '../../components/product.vue'
 import {reactive, ref} from "vue";
let seller = reactive({name: 'seller',})
let title = ref("title")
let productList = ref([])
 productList.value = [
  {
    id: 1,
    name: 'product1',
    price: 10,
    description: 'description1',
    image: 'https://picsum.photos/200/300',
  },
  {
    id: 2,
    name: 'product2',
    price: 20,
    description: 'description2',
    image: 'https://picsum.photos/200/300',
  },
  {
    id: 3,
    name: 'product3',
  },{

   },{

   },{

   },{}
 ]
</script>

<template>
    <h1>myrelease</h1>
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
        <Product :seller="seller" :title="title"></Product>
      </el-col>
    </el-row>
  </div>

</template>

<style scoped>

</style>