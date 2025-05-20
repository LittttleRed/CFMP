<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
   <Head></Head>

    <!-- 商品展示区 -->
    <div class="goods-container">
      <div v-if="loading" class="loading-wrapper">
        <el-icon class="loading-icon" :size="50"><Loading /></el-icon>
      </div>

      <div v-else class="goods-list">
        <el-row :gutter="20">
        <el-col v-for="(product, index) in homeStore.goodsList"
        :key="product.id"
        :lg="4"
        :md="8"
        :sm="12"
        :xs="24"
      >
            <Product :goods="product" />
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 分页器 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="homeStore.total"
        :pager-count="5"
        layout="prev, pager, next, jumper"
        background
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Search, Loading } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useHomeStore } from '../stores/home'
import GoodsItem from '../components/GoodsItem.vue'
import Product from "../components/product.vue";
import Head from "../components/Head.vue";



const router = useRouter()
const userStore = useUserStore()
const homeStore = useHomeStore()

const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)

// 初始化加载数据
onMounted(() => {
  fetchGoodsList()
})

// 获取商品列表
const fetchGoodsList = async () => {
  try {
    loading.value = true
    await homeStore.getGoodsList({
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: searchKeyword.value
    })
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchGoodsList()
}

// 分页变化
const handlePageChange = (val: number) => {
  currentPage.value = val
  fetchGoodsList()
}

// 用户菜单操作
const handleUserCommand = (command: string) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}

</script>

<style scoped lang="scss">
.home-container {
  min-height: 100vh;
  background-color: #f5f7fa;

  .nav-bar {
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    background: white;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    z-index: 1000;

    .nav-left {
      display: flex;
      align-items: center;
      gap: 30px;
      width: 1200px;
      margin: 0 auto;

      .logo {
        font-size: 24px;
        font-weight: bold;
        color: #0066ff;
      }

      .search-input {
        width: 400px;
      }
    }
     .nav-right {
    padding-left: 4px;
     min-width: 300px; // 与左侧保持间距
  }


  }

  .goods-container {
    max-width: 1200px;
    margin: 20px auto;
    padding: 0 20px;

    .loading-wrapper {
      text-align: center;
      padding: 100px 0;

      .loading-icon {
        animation: rotating 2s linear infinite;
      }
    }

    .goods-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 20px;
      padding: 20px 0;
    }
  }

  .pagination-wrapper {
    padding: 20px;
    display: flex;
    justify-content: center;
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>