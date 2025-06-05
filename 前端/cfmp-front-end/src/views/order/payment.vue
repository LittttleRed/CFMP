<template>
  <div class="payment-container">
    <el-card class="payment-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>订单详情</h2>
          <el-tag
            :type="getStatusType(orderDetail.status)"
            size="large"
          >
            {{ getStatusText(orderDetail.status) }}
          </el-tag>
        </div>
      </template>

      <!-- 订单基本信息 -->
      <div class="order-info-section">
        <div class="info-row">
          <span class="label">订单编号：</span>
          <span class="value">{{ orderDetail.order_id }}</span>
        </div>
        <div class="info-row">
          <span class="label">创建时间：</span>
          <span class="value">{{ formatTime(orderDetail.created_at) }}</span>
        </div>
        <div class="info-row" v-if="orderDetail.payment_time">
          <span class="label">付款时间：</span>
          <span class="value">{{ formatTime(orderDetail.payment_time) }}</span>
        </div>
        <div class="info-row" v-if="orderDetail.status === 2">
          <span class="label">完成时间：</span>
          <span class="value">{{ formatTime(orderDetail.updated_at) }}</span>
        </div>
      </div>

      <!-- 商品信息 -->
      <div class="product-section">
        <h3>商品信息</h3>
        <div v-for="item in orderDetail.products" :key="item.product_id" class="product-item">
          <el-image
            :src="item.product_image"
            fit="cover"
            class="product-thumbnail"
          >
            <template #error>
              <div class="image-error">图片加载失败</div>
            </template>
          </el-image>
          <div class="product-details">
            <h4>{{ item.product_name }}</h4>
            <div class="price-quantity">
              <span class="price">¥{{ item.price }}</span>
              <span class="quantity">x{{ item.quantity }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 卖家信息 -->
      <div class="seller-section">
        <h3>卖家信息</h3>
        <div class="seller-info">
          <span class="label">卖家账号：</span>
          <span class="value">{{ orderDetail.buyer_info?.username || '未知' }}</span>
        </div>
      </div>

      <!-- 收货地址 -->
      <div class="address-section" v-if="orderDetail.shipping_address">
        <h3>收货地址</h3>
        <div class="address-info">
          <p><strong>{{ orderDetail.shipping_name }}</strong> {{ orderDetail.shipping_phone }}</p>
          <p>{{ orderDetail.shipping_address }}</p>
          <p v-if="orderDetail.shipping_postal_code">邮编：{{ orderDetail.shipping_postal_code }}</p>
        </div>
      </div>      <!-- 金额信息 -->
      <div class="amount-section">
        <div class="amount-item">
          <span class="label">订单金额：</span>
          <span class="value amount">¥{{ orderDetail.total_amount }}</span>
        </div>
        <div class="amount-item" v-if="orderDetail.status === 1 || orderDetail.status === 2">
          <span class="label">实付款：</span>
          <span class="value amount paid">¥{{ orderDetail.total_amount }}</span>
        </div>
        <div class="amount-item" v-if="orderDetail.status === 0">
          <span class="label">应付款：</span>
          <span class="value amount pending">¥{{ orderDetail.total_amount }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button @click="goBack">返回</el-button>
        <el-button @click="goToMyOrders">我的订单</el-button>

        <!-- 根据订单状态显示不同按钮 -->
        <el-button
          v-if="orderDetail.status === 0"
          type="primary"
          @click="payNow"
        >
          立即支付
        </el-button>

        <el-button
          v-if="orderDetail.status === 0"
          type="success"
          @click="simulatePayment"
        >
          模拟支付完成
        </el-button>

        <el-button
          v-if="orderDetail.status === 0"
          type="danger"
          @click="cancelOrder"
        >
          取消订单
        </el-button>

        <el-button
          v-if="orderDetail.status === 1"
          type="success"
          @click="confirmReceived"
        >
          确认收货
        </el-button>
      </div>
    </el-card>

    <!-- 支付二维码弹窗 -->
    <el-dialog v-model="showPaymentDialog" title="扫码支付" width="400px" center>
      <div class="payment-dialog">
        <div class="qrcode-container">
          <el-image :src="paymentQrCode" class="qrcode" />
        </div>
        <p class="payment-tip">请使用{{ paymentMethodText }}扫码支付</p>
        <p class="amount-tip">支付金额：¥{{ orderDetail.total_amount }}</p>
        <div class="dialog-actions">
          <el-button @click="showPaymentDialog = false">取消</el-button>
          <el-button type="success" @click="simulatePayment">模拟支付完成</el-button>
          <el-button type="primary" @click="checkPaymentStatus">查看支付状态</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getToken } from '../../utils/user-utils.ts'
import {
  getOrderDetail,
  cancelOrder as cancelOrderApi,
  completeOrder,
  createPayment,
  queryPayment,
  simulatePaymentSuccess
} from '../../api/order/index.js'

const route = useRoute()
const router = useRouter()

const showPaymentDialog = ref(false)
const paymentQrCode = ref('')
const paymentMethodText = ref('支付宝')

// 订单详情数据
const orderDetail = reactive({
  order_id: null,
  status: 0,
  total_amount: 0,
  created_at: null,
  payment_time: null,
  updated_at: null,
  products: [],
  buyer_info: {},
  shipping_name: '',
  shipping_phone: '',
  shipping_address: '',
  shipping_postal_code: '',
  payment_method: 0
})

// 获取订单状态文本
const getStatusText = (status) => {
  const statusMap = {
    0: '待支付',
    1: '已支付',
    2: '已完成',
    3: '已取消'
  }
  return statusMap[status] || '未知状态'
}

// 获取订单状态类型
const getStatusType = (status) => {
  const typeMap = {
    0: 'warning',
    1: 'success',
    2: 'info',
    3: 'danger'
  }
  return typeMap[status] || 'info'
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  return new Date(timeStr).toLocaleString('zh-CN')
}

// 获取订单详情
const fetchOrderDetail = async () => {
  try {
    const orderId = route.query.order_id
    if (!orderId) {
      ElMessage.error('订单ID不能为空')
      return
    }

    const res = await getOrderDetail(orderId)
    console.log()
    if (res.code === 200) {
      Object.assign(orderDetail, res.data)
      console.log(orderDetail)
    } else {
      ElMessage.error(res.message || '获取订单详情失败')
    }
  } catch (error) {
    ElMessage.error('获取订单详情失败')
    console.error(error)
  }
}

// 立即支付
const payNow = async () => {
  try {
    const paymentParams = {
      order_id: orderDetail.order_id,
      total_amount: orderDetail.total_amount,
      payment_method: orderDetail.payment_method === 0 ? 'alipay' : 'wechat_pay',
      payment_subject: `订单支付: ${orderDetail.order_id}`
    }

    const res = await createPayment(paymentParams)
    if (res.code === 200) {
      // 检查是否有支付数据
      if (res.data.payment_data) {
        // 显示支付二维码
        paymentQrCode.value = res.data.payment_data.qrcode || res.data.payment_data.url
        paymentMethodText.value = orderDetail.payment_method === 0 ? '支付宝' : '微信'
        showPaymentDialog.value = true

        // 如果是重复支付请求，提示用户
        if (res.message && res.message.includes('已有未支付')) {
          ElMessage.info('检测到已有未完成的支付请求，将继续使用')
        }
      } else {
        ElMessage.error('支付数据获取失败')
      }
    } else {
      ElMessage.error(res.message || '创建支付失败')
    }
  } catch (error) {
    ElMessage.error('创建支付失败')
    console.error('支付错误:', error)
  }
}

// 取消订单
const cancelOrder = async () => {
  try {
    await ElMessageBox.confirm('确定要取消这个订单吗？', '确认取消', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const res = await cancelOrderApi(orderDetail.order_id, '用户主动取消')
    if (res.code === 200) {
      ElMessage.success('订单已取消')
      orderDetail.status = 3
    } else {
      ElMessage.error(res.message || '取消订单失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消订单失败')
      console.error(error)
    }
  }
}

// 确认收货
const confirmReceived = async () => {
  try {
    await ElMessageBox.confirm('确定已收到商品吗？', '确认收货', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'success'
    })

    const res = await completeOrder(orderDetail.order_id)
    if (res.code === 200) {
      ElMessage.success('已确认收货，订单完成')
      orderDetail.status = 2
      orderDetail.updated_at = new Date().toISOString()
    } else {
      ElMessage.error(res.message || '确认收货失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('确认收货失败')
      console.error(error)
    }
  }
}

// 检查支付状态
const checkPaymentStatus = async () => {
  try {
    const res = await queryPayment(orderDetail.order_id)
    if (res.code === 200) {
      if (res.data.status === 'success') {
        ElMessage.success('支付成功！')
        showPaymentDialog.value = false
        orderDetail.status = 1
        orderDetail.payment_time = new Date().toISOString()
      } else if (res.data.status === 'failed') {
        ElMessage.error('支付失败，请重试')
        showPaymentDialog.value = false
      } else {
        ElMessage.info('支付状态查询中，请稍后再试')
      }
    }
  } catch (error) {
    ElMessage.error('查询支付状态失败')
    console.error(error)
  }
}

// 模拟支付完成
const simulatePayment = async () => {
  try {
    ElMessageBox.confirm('确定要模拟完成支付吗？这将把订单状态更新为已支付', '模拟支付', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }).then(async () => {
      const paymentMethod = orderDetail.payment_method === 0 ? 'alipay' : 'wechat_pay'
      console.log(orderDetail.order_id)
      const res = await simulatePaymentSuccess(orderDetail.order_id, paymentMethod)

      if (res.status === 'success') {
        ElMessage.success('模拟支付成功！')
        // 更新订单状态
        orderDetail.status = 1
        orderDetail.payment_time = new Date().toISOString()
      } else {
        ElMessage.error('模拟支付失败：' + (res.message || '未知错误'))
      }
    }).catch(() => {
      // 用户取消操作
    })
  } catch (error) {
    ElMessage.error('模拟支付过程发生错误')
    console.error('模拟支付错误:', error)
  }
}

// 返回上一页
const goBack = () => {
  router.go(-1)
}

// 跳转到我的订单
const goToMyOrders = () => {
  router.push({ name: 'MyBought' })
}

onMounted(() => {
  // 检查是否已登录
  if (!getToken()) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  fetchOrderDetail()
})
</script>

<style scoped>
.payment-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.payment-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: #303133;
}

.order-info-section, .product-section, .seller-section, .address-section, .amount-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.order-info-section:last-child, .amount-section {
  border-bottom: none;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  color: #606266;
  width: 120px;
  flex-shrink: 0;
}

.value {
  color: #303133;
}

.value.amount {
  font-size: 18px;
  font-weight: bold;
}

.value.amount.paid {
  color: #67c23a;
}

.value.amount.pending {
  color: #e6a23c;
}

.product-section h3, .seller-section h3, .address-section h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 18px;
}

.product-item {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 15px;
}

.product-thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  flex-shrink: 0;
}

.product-details {
  flex: 1;
}

.product-details h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
}

.price-quantity {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  color: #e6a23c;
  font-size: 16px;
  font-weight: bold;
}

.quantity {
  color: #606266;
}

.seller-info {
  display: flex;
  gap: 10px;
}

.address-info p {
  margin: 5px 0;
  color: #303133;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
}

.payment-dialog {
  text-align: center;
}

.qrcode-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.qrcode {
  width: 200px;
  height: 200px;
}

.payment-tip {
  font-size: 16px;
  color: #606266;
  margin-bottom: 10px;
}

.amount-tip {
  font-size: 18px;
  color: #e6a23c;
  font-weight: bold;
  margin-bottom: 20px;
}

.dialog-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.image-error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background: #f5f5f5;
  color: #999;
  font-size: 12px;
}
</style>