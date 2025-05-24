<template>
  <div class="mybought-container">
    <el-container>
      <!-- 页面头部 -->
      <el-header class="page-header">
        <h2>我的购买</h2>
      </el-header>

      <!-- 主体内容 -->
      <el-main>
        <!-- 筛选标签 -->
        <div class="filter-tabs">
          <el-tabs v-model="activeTab" @tab-click="handleTabClick">
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
              <el-button type="primary" @click="$router.push('/')">去购买</el-button>
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
                    <span class="order-id">订单号：{{ order.order_id }}</span>
                    <el-tag
                      :type="getStatusTagType(order.status)"
                      class="status-tag"
                    >
                      {{ getStatusText(order.status) }}
                    </el-tag>
                  </div>
                  <div class="order-time">
                    {{ formatDate(order.created_at) }}
                  </div>
                </div>                <div class="order-content">
                  <div class="product-info">
                    <div v-if="order.items && order.items.length > 0">
                      <div
                        v-for="item in order.items"
                        :key="item.product_id"
                        class="product-item"
                      >
                        <div class="product-image">
                          <img
                            :src="item.product_image || '/default-product.png'"
                            :alt="item.product_name"
                            @error="handleImageError"
                          >
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
                      <p class="order-id-text">订单号：{{ order.order_id }}</p>
                    </div>
                  </div>

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

                <div class="order-actions">
                  <el-button
                    size="small"
                    @click.stop="viewOrderDetail(order.order_id)"
                  >
                    查看详情
                  </el-button>

                  <el-button
                    v-if="order.status === 0"
                    type="primary"
                    size="small"
                    @click.stop="payOrder(order.order_id)"
                  >
                    立即支付
                  </el-button>

                  <el-button
                    v-if="order.status === 0"
                    type="danger"
                    size="small"
                    @click.stop="showCancelDialog(order)"
                  >
                    取消订单
                  </el-button>

                  <el-button
                    v-if="order.status === 1"
                    type="success"
                    size="small"
                    @click.stop="confirmReceived(order.order_id)"
                  >
                    确认收货
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

    <!-- 取消订单对话框 -->
    <el-dialog
      v-model="cancelDialogVisible"
      title="取消订单"
      width="400px"
    >
      <div>
        <p>确定要取消订单 #{{ selectedOrder?.order_id }} 吗？</p>
        <el-form>
          <el-form-item label="取消原因">
            <el-input
              v-model="cancelReason"
              type="textarea"
              :rows="3"
              placeholder="请输入取消原因（可选）"
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelDialogVisible = false">取消</el-button>
          <el-button
            type="danger"
            @click="confirmCancel"
            :loading="cancelLoading"
          >
            确认取消
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderList, cancelOrder, completeOrder } from '../../api/order/index.js'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const orderList = ref([])
const activeTab = ref('all')
const sortOption = ref('created_desc')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 取消订单相关
const cancelDialogVisible = ref(false)
const cancelReason = ref('')
const cancelLoading = ref(false)
const selectedOrder = ref(null)

// 状态映射
const statusMap = {
  0: '待付款',
  1: '已付款',
  2: '已完成',
  3: '已取消'
}

const paymentMethodMap = {
  0: '支付宝',
  1: '微信支付'
}

// 计算属性
const getStatusText = (status) => {
  return statusMap[status] || '未知状态'
}

const getStatusTagType = (status) => {
  const typeMap = {
    0: 'warning',  // 待付款
    1: 'primary',  // 已付款
    2: 'success',  // 已完成
    3: 'info'      // 已取消
  }
  return typeMap[status] || 'info'
}

const getPaymentMethodText = (method) => {
  return paymentMethodMap[method] || '未知支付方式'
}

// 方法
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

    const response = await getOrderList(params)
    console.log('API 响应:', response) // 添加调试日志

    // 处理 DRF 分页响应格式
    if (response.results) {
      orderList.value = response.results
      total.value = response.count || 0
    } else if (response.code === 200) {
      orderList.value = response.results || response.data || []
      total.value = response.count || orderList.value.length
    } else {
      ElMessage.error(response.message || '获取订单列表失败')
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleTabClick = (tab) => {
  activeTab.value = tab.name
  currentPage.value = 1
  loadOrderList()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadOrderList()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  loadOrderList()
}

const viewOrderDetail = (orderId) => {
  router.push({
    path: '/order/payment',
    query: { order_id: orderId }
  })
}

const payOrder = (orderId) => {
  router.push({
    path: '/order/payment',
    query: { order_id: orderId }
  })
}

const showCancelDialog = (order) => {
  selectedOrder.value = order
  cancelReason.value = ''
  cancelDialogVisible.value = true
}

const confirmCancel = async () => {
  if (!selectedOrder.value) return

  cancelLoading.value = true
  try {
    const response = await cancelOrder(selectedOrder.value.order_id, cancelReason.value)

    if (response.code === 200) {
      ElMessage.success('订单已取消')
      cancelDialogVisible.value = false
      loadOrderList() // 重新加载列表
    } else {
      ElMessage.error(response.message || '取消订单失败')
    }
  } catch (error) {
    console.error('取消订单失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    cancelLoading.value = false
  }
}

const confirmReceived = async (orderId) => {
  try {
    await ElMessageBox.confirm(
      '确认收货后，订单将标记为完成，此操作不可撤销。',
      '确认收货',
      {
        confirmButtonText: '确认收货',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const response = await completeOrder(orderId)

    if (response.code === 200) {
      ElMessage.success('确认收货成功')
      loadOrderList() // 重新加载列表
    } else {
      ElMessage.error(response.message || '确认收货失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('确认收货失败:', error)
      ElMessage.error('网络错误，请稍后重试')
    }
  }
}

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

const handleImageError = (event) => {
  event.target.src = '/default-product.png'
}

// 生命周期
onMounted(() => {
  loadOrderList()
})
</script>

<style scoped>
.mybought-container {
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