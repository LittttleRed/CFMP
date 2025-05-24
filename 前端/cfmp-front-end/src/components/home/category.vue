<script setup>
import {ref} from "vue";
import {getAllCategory} from "../../api/product/index.js";

const categoryList = ref([])
const getCategoryList = async () => {
categoryList.value=await getAllCategory()
}
getCategoryList()
</script>

<template>
<div class="category-card">
  <el-card style="--el-card-border-radius: 20px;" shadow="hover">
    <h2 style="margin-left: 20px;margin-top: 0;margin-bottom: 10px" >分类</h2>
    <el-row :gutter="0">
      <el-col v-for="(category,index) in categoryList"
      :key="category.category_id"
      :lg="8"
      :md="6"
      >
        <div class="category-name" style="margin: auto;cursor: pointer;width: 40px;padding-top: 10px;padding-bottom: 10px" @click="searchWithCategory" >{{ category.name }}</div>
      </el-col>
    </el-row>
  </el-card>
</div>
</template>

<style scoped>

</style>