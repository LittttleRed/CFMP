<script setup>
import {ref} from "vue";
import {getAllCategory} from "../../api/product/index.js";
import {useRouter} from "vue-router";

const categoryList = ref([])
const router = useRouter()
const getCategoryList = async () => {
categoryList.value=await getAllCategory()
}
const searchWithCategory = (category) => {
  router.push({
    name: "search",
    query: {
      category: category.category_id,
    },
  });
};

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
      :md="8"
      :xl="8"
      :sm="8"
      :xs="8"
      >
        <div class="category-name" style="margin: auto;cursor: pointer;width: 40px;padding-top: 10px;padding-bottom: 10px" @click="searchWithCategory(category)" >{{ category.name }}</div>
      </el-col>
    </el-row>
  </el-card>
</div>
</template>

<style scoped>

</style>