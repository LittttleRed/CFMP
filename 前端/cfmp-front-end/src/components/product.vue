<template>
  <el-card class="product-card" style="--el-card-border-radius: 10px;" shadow="hover">
    <div class="image-container">
      <img :src="image" alt="商品图片" class="product-image">
    </div>

    <div class="header">
      <div class="title">
        <span class="tag">包邮</span>
        <h3 class="title-text">{{ title }}</h3>
      </div>
      <div class="price">{{ price }}</div>
    </div>
    <!-- 数据信息 -->
    <div class="stats">
     <el-avatar  :size="40" :src="seller.headimg" v-if="seller.headimg"/>
      <el-avatar :size="40" v-else>未知</el-avatar>
      <a style="margin: auto;padding-left: 20px">{{ seller.name }}</a>
    </div>
  </el-card>
</template>

<script setup>
import { StarFilled } from '@element-plus/icons-vue'

defineProps({
  title: String,
  price: String,
  mainDesc: String,
  brand: String,
  wants: Number,
  seller: {
    type: Object,
    default: () => ({
      name: '',
      headimg: ''
    })
  }
})
</script>

<style scoped>


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

.description {
  margin-bottom: 12px;
}

.main-desc {
  color: #666;
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 4px;
}

.brand {
  color: #999;
  font-size: 12px;
}


.wants {
  color: #999;
}

.seller {
  display: flex;
  align-items: center;
  color: #666;
}

.credit-icon {
  color: #ffb300;
  font-size: 14px;
  margin: 0 4px;
}

.credit-text {
  color: #ffb300;
}
</style>