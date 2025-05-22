from django.db import models
from user.models import User
from product.models import Product
from django.utils import timezone

# 订单状态常量
ORDER_STATUS_CHOICES = (
    (0, 'pending_payment'),  # 待支付
    (1, 'paid'),           # 已支付
    (2, 'completed'),      # 已完成
    (3, 'cancelled'),      # 已取消
)

# 支付方式常量
PAYMENT_METHOD_CHOICES = (
    (0, 'alipay'),       # 支付宝支付
    (1, 'wechat_pay'),   # 微信支付
)

# 支付状态常量
PAYMENT_STATUS_CHOICES = (
    (0, 'pending'),      # 待支付
    (1, 'processing'),   # 处理中
    (2, 'success'),      # 成功
    (3, 'failed'),       # 失败
    (4, 'cancelled'),    # 已取消
)

# 通知类型常量
NOTIFICATION_TYPE_CHOICES = (
    (0, 'transaction'),  # 交易通知
    (1, 'system'),       # 系统通知
    (2, 'promotion'),    # 促销通知
)

class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.SmallIntegerField(choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_time = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(blank=True, null=True)
    cancel_reason = models.TextField(blank=True, null=True)

    # 配送地址信息
    shipping_name = models.CharField(max_length=100, null=True, blank=True)
    shipping_phone = models.CharField(max_length=20, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    shipping_postal_code = models.CharField(max_length=20, null=True, blank=True)

    # def __str__(self):
    #     return f"Order {self.order_id}"
    def __str__(self):
        return str(self.payment_id)
    class Meta:
        db_table = "order"
        ordering = ['-created_at']

class OrderItem(models.Model):
    """订单商品项"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "order_item"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

class Payment(models.Model):
    """支付记录"""
    payment_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.SmallIntegerField(choices=PAYMENT_METHOD_CHOICES)
    status = models.SmallIntegerField(choices=PAYMENT_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)  # 支付平台交易号
    payment_subject = models.CharField(max_length=255)  # 支付标题
    payment_data = models.JSONField(default=dict, blank=True)  # 支付数据（如支付URL、二维码等）
    failure_reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.payment_id

    class Meta:
        db_table = "payment"
        ordering = ['-created_at']

class Notification(models.Model):
    """通知"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.SmallIntegerField(choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_id = models.CharField(max_length=50, null=True, blank=True)
    related_data = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notification"
        ordering = ['-created_at']

class SecurityPolicy(models.Model):
    """安全策略"""
    policy_id = models.CharField(max_length=50, primary_key=True)
    policy_name = models.CharField(max_length=100)
    policy_description = models.TextField()
    is_enabled = models.BooleanField(default=True)
    security_level = models.CharField(max_length=20, choices=(
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ), default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.policy_name

    class Meta:
        db_table = "security_policy"
