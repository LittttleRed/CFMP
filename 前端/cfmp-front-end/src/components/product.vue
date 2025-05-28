<template>
  <el-card class="product-card" style="--el-card-border-radius: 10px;" shadow="hover">
    <div class="image-container" style="cursor: pointer" @click="()=>{router.push({name:'product',query:{product_id:product_id,myfollow:myfollow}})}">
      <img :src="media" alt="商品图片" class="product-image" v-if="media!==null">
      <img src="https://via.placeholder.com/150" alt="商品图片" class="product-image" v-else></img>
    </div>

    <div class="header" style="cursor: pointer" @click="()=>{router.push({name:'product',query:{product_id:product_id,myfollow:myfollow}})}">
      <div class="title">
        <span class="tag" v-if="functions===0">包邮</span>
        <h3 class="title-text" >{{ title.length>12 ? title.substring(0,12)+'...' : title }}</h3>
        <div class="price" style="margin-left: 10px">{{ price }}</div>
      </div>
    </div>
    <!-- 数据信息 -->
    <div class="stats" style="cursor: pointer" @click="()=>{router.push({name:'user',query:{user_id:user_id}})}">
     <el-avatar  :size="40" :src="avatar" v-if="avatar!==null"/>
      <el-avatar :size="40"  src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" v-else></el-avatar>
      <a style="margin: auto;padding-left: 20px;font-size: 15px;font-weight: bold">{{ username }}</a>
      <el-button @click="" v-if="myfollow" class="follow"  >已关注</el-button>
    </div>

  </el-card>
</template>

<script setup>
import { StarFilled } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import {ref} from "vue";

const router = useRouter()
const route = useRoute()

defineProps({
  title: String,
  price: String,
  product_id: Number,
  user_id: Number,
  username: String,
  avatar: String,
  media: String,
  myfollow: Boolean,
  functions: Number,
})

</script>

<style scoped>
.follow{
  height:25px;
  width:50px;
  margin:auto 20px auto 20px;
  background: #ffd299;
  --el-button-border-color: #ffd299;
  color: #ff6a21
}

.image-container {
  width: 100%; /* 容器宽度为card的60% */
  height: 230px; /* 固定高度，可根据需求调整 */
  margin: 0 auto 12px; /* 水平居中 + 下边距 */
  overflow: hidden; /* 超出部分隐藏 */
  border-radius: 8px; /* 可选圆角 */
}

.product-card {
  width: 240px;
  height: 350px;
  margin: 10px;
  transition: box-shadow 0.3s;
  position: relative;
  padding-bottom: 40px;
  display: inline-flex;
  flex-direction: column;
}
.product-card .header{
  display: flex;
  font-size: 12px;
  height: 20%;
}
.product-card .stats {
  display: flex;
  font-size: 12px;
  position: absolute;
  padding-bottom: 10px;
  flex-direction: row;
}


.product-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.title {
  display: flex;
  align-items: center;
}

.tag {
  background: #ff4444;
  color: white;
  font-size: 12px;
  padding: 2px 4px;
  border-radius: 2px;
  margin-right: 8px;
}

.title-text {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.price {
  color: #ff4444;
  font-size: 18px;
  font-weight: bold;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 关键属性：保持比例填充容器 */
  transition: transform 0.3s ease; /* 添加缩放过渡效果 */
}

.product-image:hover {
  transform: scale(1.05); /* 悬停时轻微放大 */
}
</style>