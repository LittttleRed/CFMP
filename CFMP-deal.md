---
title: CFMP
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"

---

# CFMP

Base URLs:

# Authentication

# 交易模块/支付接口

## POST 创建支付请求

POST /api/payment/create

创建新的支付请求

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|query|integer| 是 |订单ID|
|total_amount|query|number| 是 |应付金额|
|payment_method|query|string| 是 |支付方式|
|payment_subject|query|string| 是 |订单标题|
|return_url|query|string| 否 |支付后跳转url|

#### 枚举值

|属性|值|
|---|---|
|payment_method|alipay|
|payment_method|wechat_pay|

> 返回示例

```json
{
  "code": 200,
  "message": "支付请求创建成功",
  "data": {
    "payment_type": "alipay",
    "payment_id": "PAY202506080001",
    "order_id": "CFMP202506080001",
    "payment_data": {
      "url": "https://openapi.alipay.com/gateway.do?token=xxxx"
    },
    "expires_at": "2025-06-08T11:15:00Z"
  }
}
```

```json
{
  "code": 200,
  "message": "支付请求创建成功",
  "data": {
    "payment_type": "wechat_pay",
    "payment_id": "PAY202506080002",
    "order_id": "CFMP202506080002",
    "payment_data": {
      "url": "https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id=xxxx",
      "qrcode": "weixin://wxpay/bizpayurl?pr=xxxx"
    },
    "expires_at": "2025-06-08T11:30:00Z"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» payment_type|string|true|none||支付方式|
|»» payment_id|string|true|none||支付ID|
|»» order_id|string|true|none||订单ID|
|»» payment_data|object|true|none||支付数据，根据不同支付方式返回不同内容|
|»»» url|string|true|none||支付宝返回支付链接|
|»»» qrcode|string|false|none||微信支付二维码数据|
|»» expires_at|string(date-time)|false|none||支付有效期|

## GET 支付回调

GET /api/payments/callback/{payment_method}

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|payment_method|path|string| 是 |支付方式|
|order_id|query|string| 否 |none|
|status|query|string| 否 |none|
|total_amount|query|number| 否 |总计金额|
|sign|query|string| 否 |支付宝或者微信返回签名|

> 返回示例

> 200 Response

```json
"success"
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» status|string|true|none||none|

## POST 支付回调

POST /api/payments/callback/{payment_method}

支付平台异步回调接口

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|payment_method|path|string| 是 |支付方式|
|order_id|query|string| 否 |订单ID|
|status|query|string| 否 |支付状态|
|total_amount|query|number| 否 |总计金额|
|sign|query|string| 否 |支付宝或者微信返回签名|
|trade_no|query|string| 否 |支付交易号（支付平台生成）|
|out_trade_no|query|string| 否 |商户订单号|
|body|body|string| 否 |none|

#### 枚举值

|属性|值|
|---|---|
|payment_method|alipay|
|payment_method|wechat_pay|

> 返回示例

> 200 Response

```json
{
  "status": "success",
  "message": "回调成功处理"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» status|string|true|none||回调处理状态|
|» message|string|false|none||回调处理消息|

## GET 支付查询

GET /api/payment/{order_id}

查询订单支付状态

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|path|string| 是 |订单ID|

> 返回示例

```json
{
  "code": 200,
  "data": {
    "order_id": "CFMP202506080001",
    "payment_id": "PAY202506080001",
    "status": "success",
    "payment_method": "alipay",
    "created_at": "2025-06-08T10:15:30Z",
    "paid_at": "2025-06-08T10:20:01Z",
    "amount": 299,
    "transaction_id": "2025060822001473030500368957",
    "products": [
      {
        "product_id": 123,
        "name": "二手笔记本电脑",
        "price": 299,
        "quantity": 1
      }
    ]
  }
}
```

```json
{
  "code": 200,
  "data": {
    "order_id": "CFMP202506080005",
    "payment_id": "PAY202506080005",
    "status": "failed",
    "payment_method": "wechat_pay",
    "created_at": "2025-06-08T16:30:00Z",
    "amount": 599,
    "products": [
      {
        "product_id": 789,
        "name": "二手相机",
        "price": 599,
        "quantity": 1
      }
    ],
    "failure_reason": "余额不足"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» order_id|string|true|none||订单ID|
|»» payment_id|string|true|none||支付ID|
|»» status|string|true|none||支付状态|
|»» payment_method|string|true|none||支付方式|
|»» created_at|string(date-time)|true|none||创建时间|
|»» paid_at|string(date-time)|false|none||支付时间|
|»» amount|number|true|none||支付金额|
|»» transaction_id|string|false|none||支付平台交易号|
|»» products|[object]|false|none||订单商品|
|»»» product_id|integer|true|none||商品ID|
|»»» name|string|false|none||商品名称|
|»»» price|number|true|none||商品价格|
|»»» quantity|integer|false|none||数量|
|»» failure_reason|string|false|none||失败原因|

#### 枚举值

|属性|值|
|---|---|
|status|pending|
|status|processing|
|status|success|
|status|failed|
|status|cancelled|
|payment_method|alipay|
|payment_method|wechat_pay|

## GET 获取支付记录列表

GET /api/payment/records

获取用户的支付记录列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|status|query|string| 否 |支付状态|
|page|query|integer| 否 |页码|
|page_size|query|integer| 否 |每页条数|
|sort|query|string| 否 |排序方式|

#### 枚举值

|属性|值|
|---|---|
|status|all|
|status|pending|
|status|success|
|status|failed|
|sort|created_desc|
|sort|created_asc|
|sort|amount_desc|
|sort|amount_asc|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "total": 15,
    "page": 1,
    "page_size": 10,
    "records": [
      {
        "payment_id": "PAY202506080001",
        "order_id": "CFMP202506080001",
        "status": "success",
        "payment_method": "alipay",
        "created_at": "2025-06-08T10:15:30Z",
        "amount": 299,
        "product_snapshot": {
          "name": "二手笔记本电脑",
          "count": 1
        }
      },
      {
        "payment_id": "PAY202506080002",
        "order_id": "CFMP202506080002",
        "status": "success",
        "payment_method": "wechat_pay",
        "created_at": "2025-06-08T14:30:45Z",
        "amount": 199,
        "product_snapshot": {
          "name": "二手手机",
          "count": 1
        }
      },
      {
        "payment_id": "PAY202506080003",
        "order_id": "CFMP202506080003",
        "status": "pending",
        "payment_method": "alipay",
        "created_at": "2025-06-08T15:45:30Z",
        "amount": 499,
        "product_snapshot": {
          "name": "多件商品",
          "count": 3
        }
      }
    ]
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» total|integer|true|none||记录总数|
|»» page|integer|true|none||当前页码|
|»» page_size|integer|true|none||每页条数|
|»» records|[object]|true|none||支付记录列表|
|»»» payment_id|string|true|none||支付ID|
|»»» order_id|string|true|none||订单ID|
|»»» status|string|true|none||支付状态|
|»»» payment_method|string|true|none||支付方式|
|»»» created_at|string(date-time)|true|none||创建时间|
|»»» amount|number|true|none||支付金额|
|»»» product_snapshot|object|false|none||商品快照|
|»»»» name|string|false|none||商品名称|
|»»»» count|integer|false|none||商品数量|

#### 枚举值

|属性|值|
|---|---|
|status|pending|
|status|processing|
|status|success|
|status|failed|
|status|cancelled|

## POST 取消支付

POST /api/payment/{payment_id}/cancel

取消未完成的支付

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|payment_id|path|string| 是 |支付ID|
|body|body|string| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "message": "支付已取消",
  "data": {
    "success": true,
    "payment_id": "PAY202506080003",
    "order_id": "CFMP202506080003",
    "status": "cancelled"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» success|boolean|true|none||是否成功|
|»» payment_id|string|true|none||支付ID|
|»» order_id|string|true|none||订单ID|
|»» status|string|true|none||当前状态|

# 交易模块/通知接口

## GET 获取通知列表

GET /api/notifications

获取用户的通知列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|type|query|string| 否 |通知类型: transaction(交易), system(系统), promotion(促销)|
|page|query|integer| 否 |页码|
|page_size|query|integer| 否 |每页条数|
|unread_only|query|boolean| 否 |是否只返回未读通知|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "total": 25,
    "page": 1,
    "page_size": 20,
    "unread_count": 5,
    "notifications": [
      {
        "id": "not_10001",
        "type": "transaction",
        "title": "订单支付成功",
        "content": "您的订单 CFMP202506080001 已成功支付，感谢您的购买！",
        "read": false,
        "created_at": "2025-06-08T10:30:00Z",
        "related_id": "CFMP202506080001"
      },
      {
        "id": "not_10002",
        "type": "system",
        "title": "系统维护通知",
        "content": "系统将于2025年6月10日凌晨2:00-4:00进行维护，期间部分功能可能无法正常使用。",
        "read": true,
        "created_at": "2025-06-07T08:00:00Z"
      },
      {
        "id": "not_10003",
        "type": "promotion",
        "title": "限时促销活动",
        "content": "618大促即将开始，多款商品限时优惠，先到先得！",
        "read": false,
        "created_at": "2025-06-06T14:00:00Z"
      }
    ]
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» total|integer|true|none||总通知数|
|»» page|integer|true|none||当前页码|
|»» page_size|integer|true|none||每页条数|
|»» unread_count|integer|true|none||未读通知数|
|»» notifications|[object]|true|none||通知列表|
|»»» id|string|true|none||通知ID|
|»»» type|string|true|none||通知类型|
|»»» title|string|true|none||通知标题|
|»»» content|string|true|none||通知内容|
|»»» read|boolean|true|none||是否已读|
|»»» created_at|string(date-time)|true|none||创建时间|
|»»» related_id|string|false|none||关联ID（如订单ID）|

#### 枚举值

|属性|值|
|---|---|
|type|transaction|
|type|system|
|type|promotion|

## GET 获取通知详情

GET /api/notifications/{notification_id}

获取通知详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|notification_id|path|string| 是 |通知ID|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "id": "not_10001",
    "type": "transaction",
    "title": "订单支付成功",
    "content": "您的订单 CFMP202506080001 已成功支付，感谢您的购买！",
    "read": true,
    "created_at": "2025-06-08T10:30:00Z",
    "related_id": "CFMP202506080001",
    "related_data": {
      "order_id": "CFMP202506080001",
      "payment_amount": 299,
      "payment_method": "alipay",
      "product_count": 1
    }
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» id|string|true|none||通知ID|
|»» type|string|true|none||通知类型|
|»» title|string|true|none||通知标题|
|»» content|string|true|none||通知内容|
|»» read|boolean|true|none||是否已读|
|»» created_at|string(date-time)|true|none||创建时间|
|»» related_id|string|false|none||关联ID|
|»» related_data|object|false|none||关联数据|

#### 枚举值

|属性|值|
|---|---|
|type|transaction|
|type|system|
|type|promotion|

## DELETE 删除通知

DELETE /api/notifications/{notification_id}

删除指定通知

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|notification_id|path|string| 是 |通知ID|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "message": "通知已删除",
  "data": {
    "success": true,
    "notification_id": "not_10001"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» success|boolean|true|none||操作是否成功|
|»» notification_id|string|true|none||通知ID|

## PUT 标记通知为已读

PUT /api/notifications/{notification_id}/read

将指定通知标记为已读

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|notification_id|path|string| 是 |通知ID|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "message": "通知已标记为已读",
  "data": {
    "success": true,
    "notification_id": "not_10001"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» success|boolean|true|none||操作是否成功|
|»» notification_id|string|true|none||通知ID|

## PUT 全部标记为已读

PUT /api/notifications/read-all

将所有通知标记为已读

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|type|query|string| 否 |通知类型: transaction(交易), system(系统), promotion(促销)|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» success|boolean|true|none||操作是否成功|
|»» count|integer|true|none||已标记为已读的通知数量|

## GET 获取未读通知数量

GET /api/notifications/unread-count

获取未读通知的数量

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|type|query|string| 否 |通知类型: transaction(交易), system(系统), promotion(促销)|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "total_unread": 7,
    "by_type": {
      "transaction": 3,
      "system": 2,
      "promotion": 2
    }
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» total_unread|integer|true|none||总未读数量|
|»» by_type|object|true|none||按类型统计的未读数量|
|»»» transaction|integer|false|none||交易相关未读通知数量|
|»»» system|integer|false|none||系统通知未读数量|
|»»» promotion|integer|false|none||促销通知未读数量|

# 交易模块/订单管理接口

## POST 创建订单

POST /api/orders

创建新的订单

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|string| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "order_id": "CFMP202506080003",
    "status": "pending_payment",
    "created_at": "2025-06-08T15:45:30Z",
    "total_amount": 499,
    "payment_url": "/api/payment/create?order_id=CFMP202506080003"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» order_id|string|true|none||订单ID|
|»» status|string|true|none||订单状态|
|»» created_at|string(date-time)|true|none||创建时间|
|»» total_amount|number|true|none||订单总金额|
|»» payment_url|string|false|none||支付链接|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|paid|
|status|completed|
|status|cancelled|

## GET 获取订单列表

GET /api/orders

获取用户的订单列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|status|query|string| 否 |订单状态|
|page|query|integer| 否 |页码|
|page_size|query|integer| 否 |每页条数|
|sort|query|string| 否 |排序方式|

#### 枚举值

|属性|值|
|---|---|
|status|all|
|status|pending_payment|
|status|paid|
|status|completed|
|status|cancelled|
|sort|created_desc|
|sort|created_asc|
|sort|amount_desc|
|sort|amount_asc|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "total": 25,
    "page": 1,
    "page_size": 10,
    "orders": [
      {
        "order_id": "CFMP202506080003",
        "status": "pending_payment",
        "created_at": "2025-06-08T15:45:30Z",
        "total_amount": 499,
        "product_count": 3,
        "product_snapshot": {
          "product_id": 123,
          "name": "二手笔记本电脑",
          "thumbnail": "https://example.com/thumbnails/laptop.jpg"
        }
      },
      {
        "order_id": "CFMP202506080002",
        "status": "paid",
        "created_at": "2025-06-08T14:30:00Z",
        "total_amount": 299,
        "product_count": 1,
        "product_snapshot": {
          "product_id": 456,
          "name": "二手手机",
          "thumbnail": "https://example.com/thumbnails/phone.jpg"
        }
      },
      {
        "order_id": "CFMP202506080001",
        "status": "completed",
        "created_at": "2025-06-08T10:15:00Z",
        "total_amount": 99,
        "product_count": 1,
        "product_snapshot": {
          "product_id": 789,
          "name": "课本",
          "thumbnail": "https://example.com/thumbnails/book.jpg"
        }
      }
    ]
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» total|integer|true|none||订单总数|
|»» page|integer|true|none||当前页码|
|»» page_size|integer|true|none||每页条数|
|»» orders|[object]|true|none||订单列表|
|»»» order_id|string|true|none||订单ID|
|»»» status|string|true|none||订单状态|
|»»» created_at|string(date-time)|true|none||创建时间|
|»»» total_amount|number|true|none||订单总金额|
|»»» product_count|integer|true|none||商品数量|
|»»» product_snapshot|object|false|none||第一个商品的快照信息|
|»»»» product_id|integer|false|none||商品ID|
|»»»» name|string|false|none||商品名称|
|»»»» thumbnail|string|false|none||商品缩略图|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|paid|
|status|completed|
|status|cancelled|

## GET 获取订单详情

GET /api/orders/{order_id}

获取订单详细信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|path|string| 是 |订单ID|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "order_id": "CFMP202506080001",
    "user_id": 10001,
    "status": "completed",
    "created_at": "2025-06-08T10:15:00Z",
    "updated_at": "2025-06-08T11:30:00Z",
    "payment_method": "alipay",
    "payment_time": "2025-06-08T10:20:00Z",
    "total_amount": 99,
    "shipping_address": {
      "name": "张三",
      "phone": "13812345678",
      "address": "北京市海淀区某大学1号楼",
      "postal_code": "100081"
    },
    "products": [
      {
        "product_id": 789,
        "name": "课本",
        "price": 99,
        "quantity": 1,
        "image": "https://example.com/images/book.jpg",
        "seller_id": 10002,
        "seller_name": "李四"
      }
    ],
    "remark": "请尽快发货"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» order_id|string|true|none||订单ID|
|»» user_id|integer|true|none||用户ID|
|»» status|string|true|none||订单状态|
|»» created_at|string(date-time)|true|none||创建时间|
|»» updated_at|string(date-time)|false|none||更新时间|
|»» payment_method|string|false|none||支付方式|
|»» payment_time|string(date-time)|false|none||支付时间|
|»» total_amount|number|true|none||订单总金额|
|»» shipping_address|object|false|none||配送地址|
|»»» name|string|false|none||收件人姓名|
|»»» phone|string|false|none||联系电话|
|»»» address|string|false|none||详细地址|
|»»» postal_code|string|false|none||邮政编码|
|»» products|[object]|true|none||商品列表|
|»»» product_id|integer|true|none||商品ID|
|»»» name|string|true|none||商品名称|
|»»» price|number|true|none||商品价格|
|»»» quantity|integer|true|none||数量|
|»»» image|string|false|none||商品图片|
|»»» seller_id|integer|true|none||卖家ID|
|»»» seller_name|string|false|none||卖家名称|
|»» remark|string|false|none||订单备注|
|»» cancel_reason|string|false|none||取消原因|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|paid|
|status|completed|
|status|cancelled|

## PUT 取消订单

PUT /api/orders/{order_id}/cancel

取消未支付的订单

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|path|string| 是 |订单ID|
|body|body|string| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "message": "订单已成功取消",
  "data": {
    "success": true,
    "order_id": "CFMP202506080003",
    "current_status": "cancelled"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» success|boolean|true|none||是否成功|
|»» order_id|string|true|none||订单ID|
|»» current_status|string|true|none||当前订单状态|

## PUT 确认收货

PUT /api/orders/{order_id}/complete

确认收货完成订单

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|order_id|path|string| 是 |订单ID|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "message": "订单已成功确认完成",
  "data": {
    "success": true,
    "order_id": "CFMP202506080002",
    "current_status": "completed"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» success|boolean|true|none||是否成功|
|»» order_id|string|true|none||订单ID|
|»» current_status|string|true|none||当前订单状态|

## GET 获取订单状态统计

GET /api/orders/stats

获取用户订单状态统计信息

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "total": 25,
    "pending_payment": 5,
    "paid": 10,
    "completed": 8,
    "cancelled": 2
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» total|integer|true|none||订单总数|
|»» pending_payment|integer|true|none||待支付订单数|
|»» paid|integer|true|none||已支付订单数|
|»» completed|integer|true|none||已完成订单数|
|»» cancelled|integer|true|none||已取消订单数|

# 交易模块/安全策略接口

## POST 风险评估

POST /api/security/risk-assessment

对交易进行风险评估

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|string| 否 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» risk_level|string|true|none||风险等级|
|»» risk_factors|[object]|true|none||风险因素列表|
|»»» factor_type|string|true|none||风险因素类型|
|»»» factor_description|string|true|none||风险因素描述|
|»»» severity|string|true|none||严重程度|
|»» recommendation|string|true|none||安全建议|

#### 枚举值

|属性|值|
|---|---|
|risk_level|low|
|risk_level|medium|
|risk_level|high|
|severity|low|
|severity|medium|
|severity|high|

## POST 欺诈检测

POST /api/security/fraud-detection

检测交易中的欺诈行为

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|string| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "fraud_score": 75,
    "fraud_detected": true,
    "fraud_types": [
      "identity_theft",
      "unusual_behavior"
    ],
    "action_recommended": "review"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» fraud_score|number|true|none||欺诈分数（0-100，越高风险越大）|
|»» fraud_detected|boolean|true|none||是否检测到欺诈|
|»» fraud_types|[string]|false|none||检测到的欺诈类型|
|»» action_recommended|string|true|none||建议采取的操作|

#### 枚举值

|属性|值|
|---|---|
|action_recommended|allow|
|action_recommended|review|
|action_recommended|block|

## GET 获取安全策略配置

GET /api/security/policies

获取系统的安全策略配置

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "data": {
    "security_level": "medium",
    "policies": [
      {
        "policy_id": "two_factor_auth",
        "policy_name": "双因素认证",
        "policy_description": "大额交易时启用双因素认证",
        "is_enabled": true
      },
      {
        "policy_id": "location_verification",
        "policy_name": "位置验证",
        "policy_description": "验证用户交易位置与常用位置的一致性",
        "is_enabled": true
      },
      {
        "policy_id": "device_tracking",
        "policy_name": "设备追踪",
        "policy_description": "监控并记录用户使用的设备信息",
        "is_enabled": false
      }
    ]
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» data|object|true|none||none|
|»» security_level|string|true|none||当前安全级别|
|»» policies|[object]|true|none||安全策略列表|
|»»» policy_id|string|true|none||策略ID|
|»»» policy_name|string|true|none||策略名称|
|»»» policy_description|string|true|none||策略描述|
|»»» is_enabled|boolean|true|none||是否启用|

#### 枚举值

|属性|值|
|---|---|
|security_level|low|
|security_level|medium|
|security_level|high|

## PUT 更新安全策略配置

PUT /api/security/policies

更新系统的安全策略配置

> Body 请求参数

```json
"string"
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|string| 否 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||HTTP状态码|
|» message|string|true|none||操作结果消息|
|» data|object|true|none||none|
|»» updated|boolean|true|none||是否更新成功|
|»» security_level|string|true|none||当前安全级别|

# 数据模型

