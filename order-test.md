# CFMP交易模块测试用例设计

## 一、支付接口测试用例

### 1. 创建支付请求

**接口路径**：POST /api/payment/create

**测试用例1.1 - 正常创建支付请求**

输入参数：
```json
{
  "order_id": 1001,
  "total_amount": 299.99,
  "payment_method": "alipay",
  "payment_subject": "购买商品",
  "return_url": "https://example.com/return"
}
```

预期输出：
```json
{
  "code": 200,
  "message": "支付请求创建成功",
  "data": {
    "payment_type": "alipay",
    "payment_id": "PAY202401010001",
    "order_id": 1001,
    "payment_data": {
      "url": "https://openapi.alipay.com/gateway.do?order_id=1001&payment_id=PAY202401010001"
    },
    "expires_at": "2024-01-01T00:30:00Z"
  }
}
```

**测试用例1.2 - 参数不完整**

输入参数：
```json
{
  "order_id": 1001,
  "payment_method": "alipay"
}
```

预期输出：
```json
{
  "code": 400,
  "message": "参数不完整"
}
```

**测试用例1.3 - 订单状态不允许支付**

输入参数：
```json
{
  "order_id": 1002, // 假设此订单已支付
  "total_amount": 199.99,
  "payment_method": "alipay",
  "payment_subject": "购买商品"
}
```

预期输出：
```json
{
  "code": 400,
  "message": "该订单状态不允许支付"
}
```

### 2. 支付回调处理

**接口路径**：POST /api/payment/callback/alipay/

**测试用例2.1 - 支付宝回调成功处理**

输入参数：
```
trade_no=2024010122001498621412341234
&out_trade_no=PAY202401010001
&order_id=1001
&status=TRADE_SUCCESS
&total_amount=299.99
&sign=XXXXXXXXXXX
```

预期输出：
```json
{
  "status": "success",
  "message": "回调成功处理"
}
```

**测试用例2.2 - 无效回调支付ID**

输入参数：
```
trade_no=2024010122001498621412341234
&out_trade_no=INVALID_ID
&status=TRADE_SUCCESS
&total_amount=299.99
&sign=XXXXXXXXXXX
```

预期输出：
```json
{
  "status": "failed",
  "message": "找不到对应的支付记录或订单"
}
```

### 3. 支付查询

**接口路径**：GET /api/payment/{order_id}/

**测试用例3.1 - 查询支付信息成功**

输入参数：
```
order_id=1001
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "order_id": "1001",
    "payment_id": "PAY202401010001",
    "status": "success",
    "payment_method": "支付宝支付",
    "created_at": "2024-01-01T00:00:00Z",
    "amount": 299.99,
    "products": [
      {
        "product_id": 101,
        "name": "商品A",
        "price": 199.99,
        "quantity": 1
      },
      {
        "product_id": 102,
        "name": "商品B",
        "price": 100,
        "quantity": 1
      }
    ],
    "paid_at": "2024-01-01T00:05:23Z",
    "transaction_id": "2024010122001498621412341234"
  }
}
```

**测试用例3.2 - 订单不存在**

输入参数：
```
order_id=9999
```

预期输出：
```json
{
  "code": 404,
  "message": "订单不存在"
}
```

### 4. 获取支付记录列表

**接口路径**：GET /api/payment/records/

**测试用例4.1 - 获取支付记录（默认排序）**

输入参数：
```
无参数（使用默认)
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 10,
    "page": 1,
    "page_size": 10,
    "records": [
      {
        "payment_id": "PAY202401010001",
        "order_id": "1001",
        "status": "success",
        "status_display": "成功",
        "payment_method": 0,
        "payment_method_display": "支付宝支付",
        "created_at": "2024-01-01T00:00:00Z",
        "amount": 299.99,
        "product_snapshot": {
          "name": "多件商品",
          "count": 2
        }
      },
      // 更多支付记录...
    ]
  }
}
```

**测试用例4.2 - 按状态筛选成功的支付记录**

输入参数：
```
status=success
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 5,
    "page": 1,
    "page_size": 10,
    "records": [
      {
        "payment_id": "PAY202401010001",
        "order_id": "1001",
        "status": "success",
        "status_display": "成功",
        "payment_method": 0,
        "payment_method_display": "支付宝支付",
        "created_at": "2024-01-01T00:00:00Z",
        "amount": 299.99,
        "product_snapshot": {
          "name": "多件商品",
          "count": 2
        }
      },
      // 更多成功的支付记录...
    ]
  }
}
```

### 5. 取消支付

**接口路径**：POST /api/payment/{payment_id}/cancel/

**测试用例5.1 - 成功取消支付**

输入参数：
```
payment_id=PAY202401010002
```

预期输出：
```json
{
  "code": 200,
  "message": "支付已取消",
  "data": {
    "success": true,
    "payment_id": "PAY202401010002",
    "order_id": "1002",
    "status": "cancelled"
  }
}
```

**测试用例5.2 - 取消不存在的支付**

输入参数：
```
payment_id=NONEXISTENT
```

预期输出：
```json
{
  "code": 404,
  "message": "支付记录不存在"
}
```

**测试用例5.3 - 取消已完成的支付**

输入参数：
```
payment_id=PAY202401010001
```

预期输出：
```json
{
  "code": 400,
  "message": "当前支付状态不可取消"
}
```

## 二、通知接口测试用例

### 1. 获取通知列表

**接口路径**：GET /api/notifications/

**测试用例1.1 - 获取所有通知**

输入参数：
```
无参数
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 15,
    "page": 1,
    "page_size": 10,
    "unread_count": 5,
    "notifications": [
      {
        "id": "1",
        "type": "transaction",
        "type_display": "交易通知",
        "title": "支付成功通知",
        "content": "您的订单 #1001 已成功支付，感谢您的购买！",
        "read": false,
        "created_at": "2024-01-01T10:00:00Z",
        "related_id": "1001"
      },
      // 更多通知...
    ]
  }
}
```

**测试用例1.2 - 按类型筛选通知**

输入参数：
```
type=transaction
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 8,
    "page": 1,
    "page_size": 10,
    "unread_count": 3,
    "notifications": [
      {
        "id": "1",
        "type": "transaction",
        "type_display": "交易通知",
        "title": "支付成功通知",
        "content": "您的订单 #1001 已成功支付，感谢您的购买！",
        "read": false,
        "created_at": "2024-01-01T10:00:00Z",
        "related_id": "1001"
      },
      // 更多交易通知...
    ]
  }
}
```

**测试用例1.3 - 只查看未读通知**

输入参数：
```
unread_only=true
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 5,
    "page": 1,
    "page_size": 10,
    "unread_count": 5,
    "notifications": [
      {
        "id": "1",
        "type": "transaction",
        "type_display": "交易通知",
        "title": "支付成功通知",
        "content": "您的订单 #1001 已成功支付，感谢您的购买！",
        "read": false,
        "created_at": "2024-01-01T10:00:00Z",
        "related_id": "1001"
      },
      // 更多未读通知...
    ]
  }
}
```

### 2. 获取通知详情

**接口路径**：GET /api/notifications/{notification_id}

**测试用例2.1 - 获取通知详情并标记为已读**

输入参数：
```
notification_id=1
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "id": "1",
    "type": "transaction",
    "type_display": "交易通知",
    "title": "支付成功通知",
    "content": "您的订单 #1001 已成功支付，感谢您的购买！",
    "read": true,
    "created_at": "2024-01-01T10:00:00Z",
    "related_id": "1001",
    "related_data": {
      "order_id": "1001",
      "payment_amount": 299.99,
      "payment_method": "支付宝支付"
    }
  }
}
```

**测试用例2.2 - 获取不存在的通知**

输入参数：
```
notification_id=999
```

预期输出：
```json
{
  "code": 404,
  "message": "通知不存在"
}
```

### 3. 删除通知

**接口路径**：DELETE /api/notifications/{notification_id}

**测试用例3.1 - 成功删除通知**

输入参数：
```
notification_id=1
```

预期输出：
```json
{
  "code": 200,
  "message": "通知已删除",
  "data": {
    "success": true,
    "notification_id": "1"
  }
}
```

**测试用例3.2 - 删除不存在的通知**

输入参数：
```
notification_id=999
```

预期输出：
```json
{
  "code": 404,
  "message": "通知不存在"
}
```

### 4. 标记通知为已读

**接口路径**：PUT /api/notifications/{notification_id}/read

**测试用例4.1 - 成功标记为已读**

输入参数：
```
notification_id=2
```

预期输出：
```json
{
  "code": 200,
  "message": "通知已标记为已读",
  "data": {
    "success": true,
    "notification_id": "2"
  }
}
```

**测试用例4.2 - 标记不存在的通知**

输入参数：
```
notification_id=999
```

预期输出：
```json
{
  "code": 404,
  "message": "通知不存在"
}
```

### 5. 全部标记为已读

**接口路径**：PUT /api/notifications/read-all

**测试用例5.1 - 标记所有通知为已读**

输入参数：
```
无参数
```

预期输出：
```json
{
  "code": 200,
  "message": "所有通知已标记为已读",
  "data": {
    "success": true,
    "count": 5
  }
}
```

**测试用例5.2 - 标记特定类型通知为已读**

输入参数：
```
type=system
```

预期输出：
```json
{
  "code": 200,
  "message": "所有通知已标记为已读",
  "data": {
    "success": true,
    "count": 2
  }
}
```

### 6. 获取未读通知数量

**接口路径**：GET /api/notifications/unread-count

**测试用例6.1 - 获取全部未读数量**

输入参数：
```
无参数
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total_unread": 5,
    "by_type": {
      "transaction": 3,
      "system": 2,
      "promotion": 0
    }
  }
}
```

**测试用例6.2 - 获取特定类型未读数量**

输入参数：
```
type=transaction
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total_unread": 3,
    "by_type": {
      "transaction": 3,
      "system": 0,
      "promotion": 0
    }
  }
}
```

## 三、订单管理接口测试用例

### 1. 创建订单

**接口路径**：POST /api/orders

**测试用例1.1 - 成功创建订单**

输入参数：
```json
{
  "products": [
    {
      "product_id": 101,
      "price": 199.99,
      "quantity": 1
    },
    {
      "product_id": 102,
      "price": 100.00,
      "quantity": 2
    }
  ],
  "shipping_name": "张三",
  "shipping_phone": "13800138000",
  "shipping_address": "北京市海淀区中关村",
  "shipping_postal_code": "100080",
  "remark": "请尽快发货",
  "total_amount": 399.99
}
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "order_id": 1003,
    "status": "pending_payment",
    "created_at": "2024-01-02T10:30:00Z",
    "total_amount": 399.99,
    "payment_url": "/api/payment/create?order_id=1003"
  }
}
```

**测试用例1.2 - 商品信息不完整**

输入参数：
```json
{
  "products": [
    {
      "product_id": 101
    }
  ],
  "shipping_name": "张三",
  "shipping_address": "北京市海淀区中关村",
  "total_amount": 199.99
}
```

预期输出：
```json
{
  "code": 400,
  "message": "请提供完整的商品信息",
  "errors": {
    "products": ["商品价格和数量是必填项"]
  }
}
```

### 2. 获取订单列表

**接口路径**：GET /api/orders

**测试用例2.1 - 获取所有订单**

输入参数：
```
无参数
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 5,
    "page": 1,
    "page_size": 10,
    "orders": [
      {
        "order_id": "1001",
        "status": "completed",
        "status_display": "已完成",
        "created_at": "2024-01-01T00:00:00Z",
        "total_amount": 299.99,
        "product_count": 2,
        "product_snapshot": {
          "product_id": 101,
          "name": "商品A",
          "thumbnail": "https://example.com/images/product_101.jpg"
        }
      },
      // 更多订单...
    ]
  }
}
```

**测试用例2.2 - 按状态筛选订单**

输入参数：
```
status=pending_payment
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 2,
    "page": 1,
    "page_size": 10,
    "orders": [
      {
        "order_id": "1003",
        "status": "pending_payment",
        "status_display": "待支付",
        "created_at": "2024-01-02T10:30:00Z",
        "total_amount": 399.99,
        "product_count": 2,
        "product_snapshot": {
          "product_id": 101,
          "name": "商品A",
          "thumbnail": "https://example.com/images/product_101.jpg"
        }
      },
      // 更多待支付订单...
    ]
  }
}
```

**测试用例2.3 - 按金额排序**

输入参数：
```
sort=amount_desc
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 5,
    "page": 1,
    "page_size": 10,
    "orders": [
      {
        "order_id": "1003",
        "status": "pending_payment",
        "status_display": "待支付",
        "created_at": "2024-01-02T10:30:00Z",
        "total_amount": 399.99,
        "product_count": 2
      },
      // 更多订单按金额降序排列...
    ]
  }
}
```

### 3. 获取订单详情

**接口路径**：GET /api/orders/{order_id}

**测试用例3.1 - 获取订单详情**

输入参数：
```
order_id=1001
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "order_id": "1001",
    "buyer": 10001,
    "buyer_info": {
      "user_id": 10001,
      "username": "user123"
    },
    "products": [
      {
        "product_id": 101,
        "product_name": "商品A",
        "price": 199.99,
        "quantity": 1,
        "product_image": "https://example.com/images/product_101.jpg"
      },
      {
        "product_id": 102,
        "product_name": "商品B",
        "price": 100.00,
        "quantity": 1,
        "product_image": "https://example.com/images/product_102.jpg"
      }
    ],
    "total_amount": 299.99,
    "status": 2,
    "status_display": "已完成",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T10:30:00Z",
    "payment_method": 0,
    "payment_method_display": "支付宝支付",
    "payment_time": "2024-01-01T00:05:23Z",
    "shipping_name": "张三",
    "shipping_phone": "13800138000",
    "shipping_address": "北京市海淀区中关村",
    "shipping_postal_code": "100080",
    "remark": "请尽快发货"
  }
}
```

**测试用例3.2 - 获取不存在的订单**

输入参数：
```
order_id=9999
```

预期输出：
```json
{
  "code": 404,
  "message": "订单不存在"
}
```

### 4. 取消订单

**接口路径**：PUT /api/orders/{order_id}/cancel

**测试用例4.1 - 成功取消订单**

输入参数：
```json
{
  "reason": "不想购买了"
}
```

路径参数：
```
order_id=1003
```

预期输出：
```json
{
  "code": 200,
  "message": "订单已成功取消",
  "data": {
    "success": true,
    "order_id": 1003,
    "current_status": "cancelled"
  }
}
```

**测试用例4.2 - 取消已支付订单**

输入参数：
```json
{
  "reason": "不需要了"
}
```

路径参数：
```
order_id=1001 // 假设此订单已支付
```

预期输出：
```json
{
  "code": 400,
  "message": "订单状态不允许取消"
}
```

### 5. 确认收货

**接口路径**：PUT /api/orders/{order_id}/complete

**测试用例5.1 - 成功确认收货**

输入参数：
```
order_id=1004 // 假设此订单已支付待收货
```

预期输出：
```json
{
  "code": 200,
  "message": "订单已成功确认完成",
  "data": {
    "success": true,
    "order_id": 1004,
    "current_status": "completed"
  }
}
```

**测试用例5.2 - 确认未支付订单**

输入参数：
```
order_id=1003 // 假设此订单未支付
```

预期输出：
```json
{
  "code": 404, 
  "message": "未找到符合条件的订单"
}
```

### 6. 获取订单状态统计

**接口路径**：GET /api/orders/stats

**测试用例6.1 - 获取订单统计**

输入参数：
```
无参数
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "total": 5,
    "pending_payment": 1,
    "paid": 1,
    "completed": 2,
    "cancelled": 1
  }
}
```

## 四、安全策略接口测试用例

### 1. 风险评估

**接口路径**：POST /api/security/risk-assessment

**测试用例1.1 - 进行风险评估**

输入参数：
```json
{
  "user_id": 10001,
  "payment_method": "alipay",
  "amount": 999.99,
  "ip_address": "123.45.67.89",
  "device_id": "device_12345",
  "location": {
    "lat": 39.9042, 
    "lng": 116.4074,
    "city": "Beijing"
  },
  "transaction_time": "2024-01-02T10:30:00Z"
}
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "risk_level": "medium",
    "risk_factors": [
      {
        "factor_type": "location",
        "factor_description": "交易地点与用户常用地点不一致",
        "severity": "medium"
      },
      {
        "factor_type": "amount",
        "factor_description": "交易金额高于用户平均交易金额",
        "severity": "low"
      }
    ],
    "recommendation": "建议进行二次身份验证"
  }
}
```

### 2. 欺诈检测

**接口路径**：POST /api/security/fraud-detection

**测试用例2.1 - 欺诈检测**

输入参数：
```json
{
  "transaction_id": "TX1001",
  "user_id": 10001,
  "payment_method": "credit_card",
  "card_info": {
    "last4": "1234",
    "bin": "411111",
    "expiry": "12/25"
  },
  "amount": 5999.99,
  "ip_address": "123.45.67.89",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "transaction_time": "2024-01-02T15:45:00Z"
}
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "fraud_score": 75,
    "fraud_detected": true,
    "fraud_types": ["identity_theft", "unusual_behavior"],
    "action_recommended": "review"
  }
}
```

### 3. 获取安全策略配置

**接口路径**：GET /api/security/policies

**测试用例3.1 - 获取安全策略**

输入参数：
```
无参数
```

预期输出：
```json
{
  "code": 200,
  "data": {
    "security_level": "medium",
    "policies": [
      {
        "policy_id": "policy_001",
        "policy_name": "强密码策略",
        "policy_description": "要求用户设置包含大小写字母、数字和特殊字符的密码",
        "is_enabled": true,
        "security_level": "high"
      },
      {
        "policy_id": "policy_002",
        "policy_name": "登录IP限制",
        "policy_description": "限制用户只能从特定IP范围登录",
        "is_enabled": false,
        "security_level": "high"
      },
      {
        "policy_id": "policy_003",
        "policy_name": "双因素认证",
        "policy_description": "重要操作需要双因素认证",
        "is_enabled": true,
        "security_level": "medium"
      }
    ]
  }
}
```

### 4. 更新安全策略配置

**接口路径**：PUT /api/security/policies/update

**测试用例4.1 - 更新安全策略**

输入参数：
```json
{
  "security_level": "high",
  "policies": [
    {
      "policy_id": "policy_001",
      "is_enabled": true
    },
    {
      "policy_id": "policy_002",
      "is_enabled": true
    },
    {
      "policy_id": "policy_003",
      "is_enabled": true
    }
  ]
}
```

预期输出：
```json
{
  "code": 200,
  "message": "安全策略更新成功",
  "data": {
    "updated": true,
    "security_level": "high"
  }
}
```

## 五、安全策略接口调整建议

根据代码审查，安全策略接口部分存在以下问题需要调整：

1. **在URL匹配问题**：`url.py`中路径为`security/policies/update/`，但`views.py`中对应的类名为`SecurityPolicyUpdateAPIView`，URL路径应该保持一致

   ```python
   # url.py 修改建议
   path('security/policies/update/', views.SecurityPolicyUpdateAPIView.as_view(), name='security-policies-update'),
   # 或者修改为更RESTful的方式
   path('security/policies/', views.SecurityPolicyUpdateAPIView.as_view(), name='security-policies-update'),
   ```

2. **风险评估和欺诈检测接口缺乏实际业务逻辑**：这两个接口目前只是返回模拟数据，建议添加实际的风险评估算法

   ```python
   class RiskAssessmentAPIView(APIView):
       """风险评估"""
       permission_classes = [IsAuthenticated]

       def post(self, request):
           # 获取评估参数
           user_id = request.data.get('user_id')
           amount = request.data.get('amount')
           payment_method = request.data.get('payment_method')
           ip_address = request.data.get('ip_address')
           location = request.data.get('location')
           
           # 执行实际的风险评估算法
           risk_score = self._calculate_risk_score(request.data)
           risk_factors = self._identify_risk_factors(request.data)
           
           # 根据风险分数确定风险等级
           if risk_score > 80:
               risk_level = "high"
           elif risk_score > 50:
               risk_level = "medium"
           else:
               risk_level = "low"
               
           return Response({
               'code': 200,
               'data': {
                   'risk_score': risk_score,
                   'risk_level': risk_level,
                   'risk_factors': risk_factors,
                   'recommendation': self._get_recommendation(risk_level)
               }
           })
       
       def _calculate_risk_score(self, data):
           # 实现风险评分算法
           # ...
           return 75  # 示例返回值
   ```

3. **安全策略接口参数校验不足**：需要添加更全面的参数验证

   ```python
   class SecurityPolicyUpdateAPIView(APIView):
       permission_classes = [IsAdminUser]
       
       def put(self, request):
           data = request.data
           security_level = data.get('security_level')
           policies = data.get('policies', [])
           
           # 参数验证
           if not security_level or security_level not in ['low', 'medium', 'high']:
               return Response({
                   'code': 400,
                   'message': '无效的安全级别',
                   'errors': {'security_level': ['必须是low、medium或high之一']}
               }, status=status.HTTP_400_BAD_REQUEST)
           
           if not policies or not isinstance(policies, list):
               return Response({
                   'code': 400,
                   'message': '无效的策略配置',
                   'errors': {'policies': ['必须提供有效的策略列表']}
               }, status=status.HTTP_400_BAD_REQUEST)
           
           # 更新策略
           # ...
   ```

4. **安全策略接口权限控制**：目前`SecurityPolicyListAPIView`没有权限控制，普通用户不应能访问系统安全策略

   ```python
   class SecurityPolicyListAPIView(APIView):
       """获取安全策略配置"""
       permission_classes = [IsAdminUser]  # 添加管理员权限限制
       
       def get(self, request):
           # ...
   ```

5. **添加安全策略创建接口**：增加创建新安全策略的功能

   ```python
   # 在views.py中添加
   class SecurityPolicyCreateAPIView(APIView):
       """创建安全策略"""
       permission_classes = [IsAdminUser]
       
       def post(self, request):
           serializer = SecurityPolicySerializer(data=request.data)
           if serializer.is_valid():
               # 生成唯一策略ID
               policy_id = f"policy_{str(uuid.uuid4())[:8]}"
               serializer.save(policy_id=policy_id)
               return Response({
                   'code': 201,
                   'message': '安全策略创建成功',
                   'data': serializer.data
               }, status=status.HTTP_201_CREATED)
           return Response({
               'code': 400,
               'message': '参数错误',
               'errors': serializer.errors
           }, status=status.HTTP_400_BAD_REQUEST)
   
   # 在url.py中添加
   path('security/policies/create/', views.SecurityPolicyCreateAPIView.as_view(), name='security-policy-create'),
   ```

实施这些调整可以提高安全策略接口的功能完整性、安全性和可用性。