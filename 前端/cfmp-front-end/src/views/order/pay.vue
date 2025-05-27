<template>
  <div class="pay-container">
    <el-card class="pay-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>确认订单</h2>
          <span class="order-id" v-if="orderData.order_id">订单号：{{ orderData.order_id }}</span>
        </div>
      </template>

      <!-- 商品信息 -->
      <div class="product-section">
        <h3>商品信息</h3>
        <div class="product-item">
          <el-image
            :src="productInfo.thumbnail"
            fit="cover"
            class="product-thumbnail"
          >
            <template #error>
              <div class="image-error">图片加载失败</div>
            </template>
          </el-image>
          <div class="product-details">
            <h4>{{ productInfo.title }}</h4>
            <p class="seller">卖家：{{ productInfo.seller_name }}</p>
            <div class="price-quantity">
              <span class="price">¥{{ productInfo.price }}</span>
              <span class="quantity">x{{ productInfo.quantity }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 收货地址 -->
      <div class="address-section">
        <h3>收货地址</h3>
        <el-form :model="addressForm" label-width="80px">
          <el-form-item label="收货人" required>
            <el-input v-model="addressForm.shipping_name" placeholder="请输入收货人姓名" />
          </el-form-item>
          <el-form-item label="手机号" required>
            <el-input v-model="addressForm.shipping_phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="收货地址" required>
            <el-input
            v-model="addressForm.shipping_address"
              type="textarea"
              placeholder="请输入详细地址"
              :rows="3"
            />
          </el-form-item>
          <el-form-item label="邮政编码">
            <el-input v-model="addressForm.shipping_postal_code" placeholder="请输入邮政编码" />
          </el-form-item>
        </el-form>
      </div>

      <!-- 订单金额 -->
      <div class="amount-section">
        <div class="amount-item">
          <span>商品金额：</span>
          <span>¥{{ (productInfo.price * productInfo.quantity).toFixed(2) }}</span>
        </div>
        <div class="amount-item">
          <span>运费：</span>
          <span>免运费</span>
        </div>
        <div class="amount-item total">
          <span>应付款：</span>
          <span class="total-amount">¥{{ totalAmount.toFixed(2) }}</span>
        </div>
      </div>

      <!-- 支付方式 -->
      <div class="payment-section">
        <h3>支付方式</h3>
        <el-radio-group v-model="paymentMethod">
          <el-radio :label="0" class="payment-option">
            <div class="payment-item">
               <!-- <img src="/alipay-icon.png" alt="支付宝" class="payment-icon" /> -->
              <span>支付宝</span>
            </div>
          </el-radio>
          <el-radio :label="1" class="payment-option">
            <div class="payment-item">
               <!-- <img src="/wechat-pay-icon.png" alt="微信支付" class="payment-icon" /> -->
              <span>微信支付</span>
            </div>
          </el-radio>
        </el-radio-group>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button size="large" @click="goBack">返回</el-button>
        <el-button
          type="primary"
          size="large"
          @click="submitOrder"
          :loading="submitting"
        >
          立即支付 ¥{{ totalAmount.toFixed(2) }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getToken, getUserId } from '../../utils/user-utils.ts'
import { getProduct } from '../../api/product/index.js'
import { createOrder, createPayment } from '../../api/order/index.js'
import {getMe} from "@/api/user/index.js";

const route = useRoute()
const router = useRouter()

const submitting = ref(false)
const paymentMethod = ref(0) // 默认支付宝

// 从路由参数获取商品信息
const productInfo = reactive({
  product_id: parseInt(route.query.product_id),
  quantity: parseInt(route.query.quantity) || 1,
  price: parseFloat(route.query.price) || 0,
  seller_id: parseInt(route.query.seller_id),
  title: '',
  thumbnail: '',
  seller_name: ''
})

// 订单数据
const orderData = reactive({
  order_id: null
})

// 收货地址表单
const addressForm = reactive({
  shipping_name: '',
  shipping_phone: '',
  shipping_address: '',
  shipping_postal_code: ''
})
const getMyAddress = async () => {
await getMe(getToken()).then((response) => {
  let user=response[0]
  addressForm.shipping_address = user["address"]
})
}
getMyAddress()
// 计算总金额
const totalAmount = computed(() => {
  return productInfo.price * productInfo.quantity
})

// 获取商品详情
const fetchProductInfo = async () => {
  try {
    const res = await getProduct(productInfo.product_id)
    productInfo.title = res.title
    productInfo.thumbnail = res.media && res.media.length > 0 ? res.media[0].media : ''
    productInfo.seller_name = res.user.username
  } catch (error) {
    ElMessage.error('获取商品信息失败')
    console.error(error)
  }
}

// 提交订单
const submitOrder = async () => {
  // 验证表单
  if (!addressForm.shipping_name || !addressForm.shipping_phone || !addressForm.shipping_address) {
    ElMessage.warning('请填写完整的收货信息')
    return
  }

  submitting.value = true

  try {
    // 创建订单
    const orderData = {
      products: [{
        product_id: productInfo.product_id,
        price: productInfo.price,
        quantity: productInfo.quantity
      }],
      total_amount: totalAmount.value,
      payment_method: paymentMethod.value,
      ...addressForm
    }
    const orderRes = await createOrder(orderData)
    console.log(orderRes)

    let orderId

    if (orderRes.code === 200) {
      // 订单创建成功
      orderId = orderRes.data.order_id
      console.log('新订单创建成功:', orderId)
    } else if (orderRes.code === 409) {
      // 存在重复订单，使用现有订单
      orderId = orderRes.data.existing_order_id
      console.log('使用现有订单:', orderId)

      if (orderRes.data.redirect_to_payment) {
        ElMessage.info('检测到该商品已有未完成订单，将使用现有订单进行支付')
      }
    } else {
      ElMessage.error(orderRes.message || '创建订单失败')
      return
    }

    // 创建支付请求
    const paymentParams = {
      order_id: orderId,
      total_amount: totalAmount.value,
      payment_method: paymentMethod.value === 0 ? 'alipay' : 'wechat_pay',
      payment_subject: `购买商品: ${productInfo.title}`
    }

    const paymentRes = await createPayment(paymentParams)
      console.log(paymentRes)
    if (paymentRes.code === 200) {
      // 跳转到支付结果页面
      router.push({
        name: 'OrderPayment',
        query: {
          order_id: orderId,
          payment_id: paymentRes.data.payment_id
        }
      })
    } else {
      ElMessage.error(paymentRes.message || '创建支付失败')
    }
  } catch (error) {
    ElMessage.error('提交订单失败，请重试')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 返回上一页
const goBack = () => {
  router.go(-1)
}

onMounted(() => {
  // 检查是否已登录
  if (!getToken()) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  // 检查必要参数
  if (!productInfo.product_id || !productInfo.price) {
    ElMessage.error('商品信息不完整')
    router.go(-1)
    return
  }

  fetchProductInfo()
})
</script>

<style scoped>
.pay-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.pay-card {
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

.order-id {
  color: #909399;
  font-size: 14px;
}

.product-section, .address-section, .amount-section, .payment-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.product-section h3, .address-section h3, .payment-section h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 18px;
}

.product-item {
  display: flex;
  gap: 15px;
  align-items: center;
}

.product-thumbnail {
  width: 100px;
  height: 100px;
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

.seller {
  color: #909399;
  margin: 0 0 8px 0;
  font-size: 14px;
}

.price-quantity {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  color: #e6a23c;
  font-size: 18px;
  font-weight: bold;
}

.quantity {
  color: #606266;
}

.amount-section {
  background-color: #fafafa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.amount-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.amount-item.total {
  font-size: 16px;
  font-weight: bold;
  border-top: 1px solid #ebeef5;
  padding-top: 8px;
  margin-top: 8px;
}

.total-amount {
  color: #e6a23c;
  font-size: 20px;
}

.payment-option {
  display: block;
  margin-bottom: 10px;
}

.payment-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.payment-icon {
  width: 24px;
  height: 24px;
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: flex-end;
  margin-top: 30px;
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