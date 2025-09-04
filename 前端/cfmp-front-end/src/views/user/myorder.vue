<template>
  <div class="mysold-container">
    <el-container>
      <!-- 页面头部 -->
      <el-header class="page-header">
        <h2>我的订单</h2>
      </el-header>

      <!-- 主体内容 -->
      <el-main>
        <!-- 筛选标签 -->
        <div class="filter-tabs">
          <el-tabs v-model="activeTab" @tab-change="handleTabChange">
            <el-tab-pane label="全部" name="all"></el-tab-pane>
            <el-tab-pane label="待付款" name="pending_payment"></el-tab-pane>
            <el-tab-pane label="已付款" name="paid"></el-tab-pane>
            <el-tab-pane label="已完成" name="completed"></el-tab-pane>
            <el-tab-pane label="已取消" name="cancelled"></el-tab-pane>
          </el-tabs>
        </div>

        <!-- 排序选项 -->
        <div class="sort-options">
          <el-select v-model="sortOption" @change="loadOrderList" placeholder="排序方式">
            <el-option label="创建时间（从新到旧）" value="created_desc"></el-option>
            <el-option label="创建时间（从旧到新）" value="created_asc"></el-option>
            <el-option label="金额（从高到低）" value="amount_desc"></el-option>
            <el-option label="金额（从低到高）" value="amount_asc"></el-option>
          </el-select>
        </div>

        <!-- 订单列表 -->
        <div class="order-list" v-loading="loading">
          <div v-if="orderList.length === 0 && !loading" class="empty-state">
            <el-empty description="暂无订单">
              <el-button type="primary" @click="$router.push('/')">去首页看看</el-button>
            </el-empty>
          </div>

          <div v-else>
            <div
              v-for="order in orderList"
              :key="order.order_id"
              class="order-item"
              @click="viewOrderDetail(order.order_id)"
            >
              <el-card shadow="hover" class="order-card">
                <div class="order-header">
                  <div class="order-info">
                    <span class="order-id" :title="order.order_id">订单号：{{ order.order_id }}</span>
                    <el-tag :type="getStatusTagType(order.status)" class="status-tag">
                      {{ getStatusText(order.status) }}
                    </el-tag>
                  </div>
                  <div class="order-time">{{ formatDate(order.created_at) }}</div>
                </div>

                <div class="order-content">
                  <!-- 买家信息 -->
                  <div class="buyer-info">
                    <div class="buyer-details">
                      <p>电话：{{ order.shipping_phone }}</p>
                      <p>地址：{{ order.shipping_address }}</p>
                    </div>
                  </div>

                  <!-- 商品信息 -->
                  <div class="product-info">
                    <div v-if="order.products && order.products.length > 0">
                      <div
                        v-for="item in order.products"
                        :key="item.product_id"
                        class="product-item"
                      >
                        <div class="product-image">
                          <img
                            :src="item.product_image || '/placeholder-image.png'"
                            :alt="item.product_name"
                            @error="handleImageError"
                          />
                        </div>
                        <div class="product-details">
                          <h4 class="product-name">{{ item.product_name }}</h4>
                          <div class="product-meta">
                            <span class="price">¥{{ item.price }}</span>
                            <span class="quantity">x{{ item.quantity }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-else class="no-products">
                      <p>订单商品信息缺失</p>
                    </div>
                  </div>

                  <!-- 总结 -->
                  <div class="order-summary">
                    <div class="total-amount">
                      <span>总金额：</span>
                      <span class="amount">¥{{ order.total_amount }}</span>
                    </div>
                    <div class="payment-method" v-if="order.payment_method !== null">
                      <span>支付方式：{{ getPaymentMethodText(order.payment_method) }}</span>
                    </div>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="order-actions">
                  <el-button size="small" @click.stop="viewOrderDetail(order.order_id)">
                    查看详情
                  </el-button>
                </div>
              </el-card>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="total > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import {createRouter as $router, useRouter} from 'vue-router'
import { ElMessage } from 'element-plus'
import { getOrderSoldList } from '../../api/order/index.js'
import { createImageErrorHandler } from '../../utils/imageErrorHandler.js'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const orderList = ref([])
const activeTab = ref('all')
const sortOption = ref('created_desc')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 状态映射
const statusMap = {
  0: '待付款',
  1: '已付款',
  2: '已完成',
  3: '已取消'
}

// 支付方式映射
const paymentMethodMap = {
  0: '支付宝',
  1: '微信支付'
}

// 获取状态文本
const getStatusText = (status) => {
  return statusMap[status] || '未知状态'
}

// 获取 tag 类型
const getStatusTagType = (status) => {
  const typeMap = {
    0: 'warning',
    1: 'primary',
    2: 'success',
    3: 'info'
  }
  return typeMap[status] || 'info'
}

// 获取支付方式文本
const getPaymentMethodText = (method) => {
  return paymentMethodMap[method] || '未知支付方式'
}

// 加载订单列表
const loadOrderList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      sort: sortOption.value
    }

    if (activeTab.value !== 'all') {
      params.status = activeTab.value
    }

    const response = await getOrderSoldList(params)
    console.log('API响应:', response)
    orderList.value = response.results.data || []
    console.log('订单列表:', orderList.value)
    total.value = response.count || 0

    // 添加调试信息，查看订单数据结构
    if (orderList.value.length > 0) {
      console.log('第一个订单的完整数据:', JSON.stringify(orderList.value[0], null, 2))
      if (orderList.value[0].items && orderList.value[0].items.length > 0) {
        console.log('第一个商品项数据:', JSON.stringify(orderList.value[0].items[0], null, 2))
      }
    }

    // 如果列表为空且不是首页，可能是页码太大，自动回到第一页
    if (orderList.value.length === 0 && currentPage.value > 1) {
      currentPage.value = 1
      await loadOrderList()
      return
    }
  } catch (error) {
    console.error('加载订单失败:', error)
    ElMessage.error('加载订单失败，请稍后再试')
    orderList.value = [] // 出错时清空列表
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 标签切换事件
const handleTabChange = (tabName) => {
  activeTab.value = tabName
  currentPage.value = 1
  loadOrderList()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadOrderList()
}

// 当前页码变化
const handleCurrentChange = (page) => {
  currentPage.value = page
  loadOrderList()
}

// 查看订单详情
const viewOrderDetail = (orderId) => {
  router.push({
    path: '/order/payment',
    query: { order_id: orderId }
  })
}

// 时间格式化
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 图片错误处理 - 使用工具函数
const handleImageError = createImageErrorHandler()

// 初始化订单页面
const initOrderPage = () => {
  // 首先重置所有状态，避免之前的状态影响
  orderList.value = []
  total.value = 0
  currentPage.value = 1

  // 从URL参数中获取初始标签，如果没有则默认为'all'
  const urlParams = new URLSearchParams(window.location.search)
  const tabParam = urlParams.get('tab')

  // 验证标签是否有效
  const validTabs = ['all', 'pending_payment', 'paid', 'completed', 'cancelled']
  if (tabParam && validTabs.includes(tabParam)) {
    activeTab.value = tabParam
  } else {
    activeTab.value = 'all'
  }

  console.log('初始化我的订单页面，设置选中标签为:', activeTab.value)

  // 使用Vue的nextTick确保DOM已更新后再加载数据
  nextTick(() => {
    console.log('DOM更新完成，开始加载订单列表')
    loadOrderList()
  })
}

onMounted(() => {
  initOrderPage()
})
</script>

<style scoped>
.mysold-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  padding: 0 0 20px 0;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.filter-tabs {
  margin-bottom: 20px;
}

.sort-options {
  margin-bottom: 20px;
  text-align: right;
}

.order-list {
  min-height: 400px;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

.order-item {
  margin-bottom: 16px;
  cursor: pointer;
}

.order-card {
  transition: all 0.3s ease;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.order-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-id {
  font-weight: 500;
  color: #303133;
}

.status-tag {
  font-size: 12px;
}

.order-time {
  color: #909399;
  font-size: 14px;
}

.order-content {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.product-info {
  flex: 1;
}

.product-item {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-details {
  flex: 1;
}

.product-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  line-height: 1.4;
}

.product-desc {
  margin: 0 0 8px 0;
  color: #909399;
  font-size: 14px;
  line-height: 1.4;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  color: #f56c6c;
  font-weight: 500;
  font-size: 16px;
}

.quantity {
  color: #909399;
  font-size: 14px;
}

.order-summary {
  min-width: 150px;
  text-align: right;
}

.total-amount {
  margin-bottom: 8px;
}

.amount {
  color: #f56c6c;
  font-weight: 600;
  font-size: 18px;
}

.payment-method {
  color: #909399;
  font-size: 14px;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.pagination-wrapper {
  margin-top: 40px;
  text-align: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.no-products {
  padding: 20px;
  text-align: center;
  color: #909399;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px dashed #dcdfe6;
}

.no-products p {
  margin: 5px 0;
}

.order-id-text {
  font-size: 12px;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mybought-container {
    padding: 10px;
  }

  .order-content {
    flex-direction: column;
  }

  .order-summary {
    text-align: left;
  }

  .order-actions {
    justify-content: center;
  }

  .sort-options {
    text-align: left;
  }
}
</style>