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
          <!-- 使用更可靠的方式处理标签切换 -->
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
                      >                        <div class="product-image">
                          <img
                            :src="item.product_image || '/placeholder-image.png'"
                            :alt="item.product_name || '商品图片'"
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
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
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

// 状态映射 - 数字状态码到中文显示文本的映射
const statusMap = {
  0: '待付款',
  1: '已付款',
  2: '已完成',
  3: '已取消'
}

// 反向映射 - 状态码到字符串状态名的映射
const statusCodeToStringMap = {
  0: 'pending_payment',
  1: 'paid',
  2: 'completed',
  3: 'cancelled'
}

const paymentMethodMap = {
  0: '支付宝',
  1: '微信支付'
}

// 获取状态文本
const getStatusText = (status) => {
  return statusMap[status] || '未知状态'
}

// 根据标签名获取状态文本
const getStatusTextByTab = (tabName) => {
  if (tabName === 'all') return '全部'

  // 标签名本身就是状态字符串
  const statusMap = {
    'pending_payment': '待付款',
    'paid': '已付款',
    'completed': '已完成',
    'cancelled': '已取消'
  }

  return statusMap[tabName] || '未知状态'
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

// 加载订单列表方法
const loadOrderList = async () => {
  loading.value = true

  // 清空当前列表，避免数据混合
  orderList.value = []

  try {
    // 构建API请求参数
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      sort: sortOption.value
    }

    // 'all'标签不传status参数，其他标签直接传递标签名称作为状态参数
    if (activeTab.value && activeTab.value !== 'all') {
      params.status = activeTab.value
    }
      // 增强调试信息
    console.log('正在获取订单列表，当前标签:', activeTab.value)
    console.log('查询参数:', JSON.stringify(params))

    // 发起API请求
    const response = await getOrderList(params)
      // 处理响应数据
    console.log('API响应:', response)    // 更新订单列表和总数
    orderList.value = response.results.data || []
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
    console.error('加载订单列表时出错:', error)
    ElMessage.error('加载订单列表失败，请稍后重试')
    orderList.value = [] // 出错时清空列表
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 使用更简单可靠的tab-change事件处理函数
const handleTabChange = (tabName) => {
  // tabName参数直接是选中标签的name值，不需要从复杂对象中提取
  console.log('标签切换为:', tabName)

  // 切换标签时重置到第一页
  currentPage.value = 1

  // 直接加载订单列表
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
    console.log('取消订单响应:', response)
    console.log('响应状态码类型:', typeof response.code)
    console.log('响应状态码值:', response.code)

    // 检查成功条件：有明确的成功状态码 或者 消息表明操作成功
    const isSuccess =
      response.code === 200 ||
      response.code === '200' ||
      response.status === 200 ||
      response.status === '200' ||
      (response.message && (
        response.message.includes('订单已取消') ||
        response.message.includes('取消成功') ||
        response.message.includes('成功')
      ))

    if (isSuccess) {
      ElMessage.success(response.message || '订单已取消')
      cancelDialogVisible.value = false
      loadOrderList() // 重新加载列表
    } else {
      console.log('取消订单失败 - 状态码:', response.code, '消息:', response.message)
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

    // 检查成功条件：有明确的成功状态码 或者 消息表明操作成功
    const isSuccess =
      response.code === 200 ||
      response.code === '200' ||
      response.status === 200 ||
      response.status === '200' ||
      (response.message && (
        response.message.includes('确认收货成功') ||
        response.message.includes('收货成功') ||
        response.message.includes('订单完成') ||
        response.message.includes('成功')
      ))

    if (isSuccess) {
      ElMessage.success(response.message || '确认收货成功')
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
  // 设置默认图片，使用本地资源
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDE1MCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik03NSA0NEM2Ny4yNjggNDQgNjEgNTAuMjY4IDYxIDU4UzY3LjI2OCA3MiA3NSA3MlM4OSA2NS43MzIgODkgNThTODIuNzMyIDQ0IDc1IDQ0WiIgZmlsbD0iI0NDQ0NDQyIvPgo8cGF0aCBkPSJNMTI1IDEwNkg5MC4yNzMyIDc1IDU5LjcyNjggMjVWMTA2SDE1VjEyNUgxMjVWMTA2WiIgZmlsbD0iI0NDQ0NDQyIvPgo8dGV4dCB4PSI3NSIgeT0iODAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5OTk5OTkiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxMiI+5pqC5peg5Zu+54mHPC90ZXh0Pgo8L3N2Zz4K'
  console.log('商品图片加载失败，使用默认图片')
}

// 初始化函数 - 确保标签状态是正确的
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

  console.log('初始化订单页面，设置选中标签为:', activeTab.value)

  // 使用Vue的nextTick确保DOM已更新后再加载数据
  // 这样可以确保标签选中状态已经在DOM中反映出来
  nextTick(() => {
    console.log('DOM更新完成，开始加载订单列表')
    loadOrderList()
  })
}

// 生命周期
onMounted(() => {
  initOrderPage()
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