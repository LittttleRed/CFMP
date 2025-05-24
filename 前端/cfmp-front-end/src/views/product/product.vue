<template>
  <Head></Head>
  <div class="product-container">
    <!-- 商品主内容卡片 -->
    <el-card shadow="hover" class="product-card">
      <!-- 商品图片和基本信息 -->
      <div class="main-content">
        <!-- 商品主图 -->
        <el-button class="btn" style="margin: auto;font-size: 20px;font-weight: bold"
        @click="imgindex===0?imgindex=productData.media.length-1:imgindex--"><</el-button>
        <el-image
          :src="productData.media[imgindex]"
          :preview-src-list="productData.media"
          fit="cover"
          class="product-image"
        >

          <template #error>
            <div class="image-error">图片加载失败</div>
          </template>
        </el-image>
        <el-button class="btn" style="margin: auto;font-size: 20px;font-weight: bold"
        @click="imgindex===productData.media.length-1?imgindex=0:imgindex++">></el-button>

        <!-- 商品信息 -->
        <div class="product-info">
          <!-- 标题区 -->
          <div class="title-section">
            <h1 class="product-title">{{ productData.title }}</h1>
          </div>

          <!-- 价格区 -->
          <div class="price-section" style="margin-top: 50%">
            <span class="current-price">¥{{ productData.price }}</span>
          </div>
          <!-- 操作按钮 -->
          <div class="action-buttons">
            <el-button
              type="success"
              size="large"
              @click="showPurchaseDialog = true"
            >
              立即购买
            </el-button>
            <el-button
            type="warning"
            size="large"
            v-if="productData.user.user_id==getUserId()"
            @click="change"
            >
              修改
            </el-button>
             <el-button
            type="warning"
            size="large"
            v-if="productData.user.user_id!=getUserId()&&!isCollected"
            @click="collect"
            >
              收藏
            </el-button>
            <el-button
            type="warning"
            size="large"
            v-if="productData.user.user_id!=getUserId()&&isCollected"
            @click="uncollect"
            >
              取消收藏
            </el-button>
          </div>
        </div>
      </div>

      <!-- 商品详情 -->
      <el-divider content-position="left">商品详情</el-divider>
      <div class="user" style="display: flex;flex-direction: row;">
        <el-avatar :src="productData.user.avatar" size="large"></el-avatar>
        <div @click="()=>{router.push({name:'user',query:{user_id:productData.user.user_id}})}"
             style="cursor:  pointer;margin-left: 15px;margin-top: auto;margin-bottom: auto;font-weight: bold;font-size: 20px">
          {{ productData.user.username }}
          <el-button style="background:#ffd364;border:none;margin: auto auto auto 20px;">关注</el-button>
        </div>

      </div>
      <div class="product-detail" v-html="productData.description"></div>
    </el-card>

    <!-- 评论区域 -->
    <el-card shadow="hover" class="comment-section">
      <template #header>
        <div class="comment-header">
          <span>用户评价（{{ productData.comments.length }}）</span>
          <el-button type="primary" plain @click="showCommentDialog = true">
            发表评价
          </el-button>
        </div>
      </template>

      <!-- 评论列表 -->
      <div
        v-for="comment in productData.comments"
        :key="comment.id"
        class="comment-item"
        v-if="getToken()"
      >
        <div class="user-info">
          <el-avatar :src="comment.avatar" />
          <span class="username">{{ comment.username }}</span>
          <el-rate
            v-model="comment.rating"
            disabled
            show-score
            score-template="{value} 分"
          />
        </div>
        <div class="comment-content">{{ comment.content }}</div>
        <el-divider />
      </div>
      <div class="comment-item" v-else></div>
    </el-card>

    <!-- 购买对话框 -->
    <el-dialog v-model="showPurchaseDialog" title="确认购买">
      <div class="purchase-dialog">
        <el-form label-width="80px">
          <el-form-item label="购买数量">
            <el-input-number
              v-model="purchaseQuantity"
              :min="1"
              :max="productData.stock"
            />
            <span class="stock">库存：{{ productData.stock }}件</span>
          </el-form-item>
        </el-form>
        <div class="dialog-footer">
          <el-button @click="showPurchaseDialog = false">取消</el-button>
          <el-button type="primary" @click="handlePurchase">支付</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ShoppingCart } from '@element-plus/icons-vue'
import {useRoute} from "vue-router";
import {checkCollection, getProduct} from "../../api/product/index.js";
import {getToken, getUserId} from "../../utils/user-utils.js";
import Head from "../../components/Head.vue";
import {ElMessage} from "element-plus";
import router from "../../router/index.js";
const route = useRoute()
const product_id = route.query.product_id
const imgindex = ref(0)
const isMyProduct  = ref(false)
const isCollected = ref(false)
const initProduct=async (id) => {
  await getProduct(id).then(res => {
    console.log(res)
    productData.title = res.title
    productData.price = res.price
    productData.description  = res.description
    productData.media = res.media.map(item =>item.media)
    productData.main_image = productData.media[0]
    productData.user = res.user
    console.log(res.user)
    if(res.user.user_id===getUserId()){
      isMyProduct.value = true
    }
    console.log(productData)

  })

}
checkCollection(product_id,getToken()).then(
        res=>{
          isCollected.value = res.is_collected
        }
    )
initProduct(product_id)
// 模拟商品数据
const productData = reactive({
  product_id: product_id,
  title: '【官方正品】高端智能手机 旗舰款',
  price: 5999.00,
  main_image: 'http://59.110.23.64:9000/img/product_media/4272732bfeaf7a432e9cf1c4148bc1cd6e.jpg',
  media: [
    'http://59.110.23.64:9000/img/product_media/4272732bfeaf7a432e9cf1c4148bc1cd6e.jpg',
  ],
  description: '高端旗舰手机，采用最新处理器...',
  user: {
    user_id: 1,
    username: 'username',
    avatar: ''
  },
  comments: [
    {
      id: 1,
      username: '用户1',
      avatar: 'https://example.com/avatar1.jpg',
      rating: 4.5,
      content: '手机性能非常强大，运行流畅'
    },
    // 更多评论...
  ]
})

// 交互状态
const showPurchaseDialog = ref(false)
const purchaseQuantity = ref(1)
const showCommentDialog = ref(false)

const collect = () => {
  ElMessage.success('收藏成功')
}
const uncollect = () => {
  ElMessage.success('取消收藏成功')
}
const handlePurchase = () => {
  showPurchaseDialog.value = false
  ElMessage.success('购买成功')
}
</script>

<style scoped>
.user{

}
.product-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.product-card {
  margin-bottom: 20px;
}

.main-content {
  display: flex;
  gap: 30px;
}

.product-image {
  width: 500px;
  height: 500px;
  border-radius: 8px;
}

.product-info {
  flex: 1;
}

.title-section {
  margin-bottom: 20px;
}

.product-title {
  font-size: 24px;
  margin: 0 0 10px 0;
}

.status-tags {
  display: flex;
  gap: 10px;
}

.price-section {
  margin-bottom: 30px;
}

.current-price {
  font-size: 32px;
  color: #ff4444;
  margin-right: 15px;
}

.nav-buttons {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  padding: 0 16px;
}

.btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: rgba(255, 255, 255, 1);
}

.btn i {
  font-size: 20px;
  color: #333;
}

.action-buttons {
  margin-top: 40px;
  display: flex;
  gap: 20px;
}

.product-detail {
  padding: 20px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-item {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.username {
  font-weight: bold;
}

.comment-content {
  color: #666;
  line-height: 1.6;
}

.purchase-dialog {
  .stock {
    margin-left: 20px;
    color: #666;
  }

  .dialog-footer {
    text-align: right;
    margin-top: 20px;
  }
}

.image-error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background: #f5f5f5;
  color: #999;
}
</style>