<template>
  <div class="goods-item">
    <div class="cover-wrapper">
      <img :src="data.cover" alt="商品封面" class="cover" />
    </div>
    <div class="info">
      <h3 class="title">{{ data.title }}</h3>
      <p class="price">¥{{ data.price.toFixed(2) }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  data: {
    id: number
    title: string
    price: number
    cover: string
  }
}>()
</script>

<style scoped lang="scss">
.goods-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s;
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
  }

  .cover-wrapper {
    aspect-ratio: 1/1;
    background: #f5f7fa;

    .cover {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .info {
    padding: 12px;

    .title {
      font-size: 14px;
      color: #333;
      margin-bottom: 8px;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      overflow: hidden;
    }

    .price {
      color: #ff4444;
      font-size: 16px;
      font-weight: bold;
    }
  }
}
</style>