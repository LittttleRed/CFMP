import http from "../../utils/request.js";

// 订单相关API
export const createOrder = (data) => {
    return http({
        url: 'orders/',
        method: 'post',
        data: data
    })
}

export const getOrderList = (params = {}) => {
    return http({
        url: 'orders/',
        method: 'get',
        params: params
    })
}

export const getOrderDetail = (orderId) => {
    return http({
        url: `orders/${orderId}/`,
        method: 'get'
    })
}

export const cancelOrder = (orderId, reason = '') => {
    return http({
        url: `orders/${orderId}/cancel/`,
        method: 'post',
        data: { reason }
    })
}

export const completeOrder = (orderId) => {
    return http({
        url: `orders/${orderId}/complete/`,
        method: 'patch'
    })
}

export const getOrderStats = () => {
    return http({
        url: 'orders/stats/',
        method: 'get'
    })
}

// 支付相关API
export const createPayment = (data) => {
    return http({
        url: 'payment/create/',
        method: 'post',
        data: data
    })
}

export const queryPayment = (orderId) => {
    return http({
        url: `payment/${orderId}/`,
        method: 'get'
    })
}

export const getPaymentRecords = (params = {}) => {
    return http({
        url: 'payment/records/',
        method: 'get',
        params: params
    })
}

export const cancelPayment = (paymentId) => {
    return http({
        url: `payment/${paymentId}/cancel/`,
        method: 'post'
    })
}

export const refundOrder = (orderUuid, data) => {
    return http({
        url: `payment/${orderUuid}/refund/`,
        method: 'post',
        data: data
    })
}

// 模拟支付完成的API
export const simulatePaymentSuccess = (orderUuid, paymentMethod = 'alipay', paymentId) => {
    return http({
        url: `payment/callback/${paymentMethod}/`,
        method: 'post',
        data: {
            order_uuid: orderUuid,  // 订单UUID（字符串）
            payment_id: paymentId,    // 支付记录ID
            transaction_id: Date.now().toString(),
            status: 'success',
            total_amount: 0,  // 实际金额会在后端查询
            sign: 'simulated_signature'
        }
    })
}

// 通知相关API
export const getNotifications = (params = {}) => {
    return http({
        url: 'notifications/',
        method: 'get',
        params: params
    })
}

export const getNotificationDetail = (notificationId) => {
    return http({
        url: `notifications/detail/${notificationId}/`,
        method: 'get'
    })
}

export const markNotificationRead = (notificationId) => {
    return http({
        url: `notifications/${notificationId}/read/`,
        method: 'patch'
    })
}

export const markAllNotificationsRead = (type = null) => {
    return http({
        url: 'notifications/read-all/',
        method: 'patch',
        params: type ? { type } : {}
    })
}

export const deleteNotification = (notificationId) => {
    return http({
        url: `notifications/${notificationId}/`,
        method: 'delete'
    })
}

export const getUnreadCount = (type = null) => {
    return http({
        url: 'notifications/unread-count/',
        method: 'get',
        params: type ? { type } : {}
    })
}
export const getOrderSoldList = async (params) => {
    return http({
      url: 'orders/sold/',
      method: 'get',
      params: params
    })
}