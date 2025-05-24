from rest_framework import serializers
from .models import Order, OrderItem, Payment, Notification, SecurityPolicy
from product.serializers import ProductSerializer
from user.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.product_id', read_only=True)
    product_name = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'price', 'quantity', 'product_image']

    def get_product_image(self, obj):
        if hasattr(obj.product, 'product_img') and obj.product.product_img:
            return obj.product.product_img
        return None


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(source='order_items', many=True, read_only=True)
    buyer_info = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'buyer', 'buyer_info', 'products', 'total_amount',
                  'status', 'status_display', 'created_at', 'updated_at',
                  'payment_method', 'payment_method_display', 'payment_time',
                  'shipping_name', 'shipping_phone', 'shipping_address',
                  'shipping_postal_code', 'remark', 'cancel_reason']
        read_only_fields = ['order_id', 'created_at', 'updated_at', 'payment_time']

    def get_buyer_info(self, obj):
        return {
            'user_id': obj.buyer.user_id,
            'username': obj.buyer.username,
        }


class CreateOrderSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Order
        fields = ['products','total_amount', 'payment_method', 'remark',
                  'shipping_name', 'shipping_phone', 'shipping_address',
                  'shipping_postal_code']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        buyer = self.context['request'].user

        # 创建订单
        order = Order.objects.create(
            buyer=buyer,
            status=0,  # 默认状态为待支付
            **validated_data
        )

        # 创建订单项
        for product_item in products_data:
            try:
                OrderItem.objects.create(
                    order=order,
                    product_id=product_item['product_id'],
                    price=product_item['price'],
                    quantity=product_item['quantity']
                )
            except Exception as e:
                # 如果创建订单项失败，删除已创建的订单
                order.delete()
                raise serializers.ValidationError(f"创建订单项失败: {str(e)}")

        return order


class OrderListSerializer(serializers.ModelSerializer):
    """用于列表展示的简化订单序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'status', 'status_display', 'created_at', 'updated_at',
                  'total_amount', 'payment_method', 'payment_method_display',
                  'payment_time', 'items', 'remark', 'cancel_reason']


class PaymentSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    order_id = serializers.IntegerField(source='order.order_id', read_only=True)

    class Meta:
        model = Payment
        fields = ['payment_id', 'order_id', 'amount', 'payment_method', 'payment_method_display',
                  'status', 'status_display', 'created_at', 'paid_at', 'expires_at',
                  'transaction_id', 'payment_subject', 'payment_data', 'failure_reason']
        read_only_fields = ['payment_id', 'created_at', 'paid_at']


class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=['alipay', 'wechat_pay'])
    payment_subject = serializers.CharField()
    return_url = serializers.CharField(required=False)


class PaymentListSerializer(serializers.ModelSerializer):
    """用于列表展示的简化支付记录序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    order_id = serializers.IntegerField(source='order.order_id')
    product_snapshot = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['payment_id', 'order_id', 'status', 'status_display',
                  'payment_method', 'payment_method_display', 'created_at',
                  'amount', 'product_snapshot']

    def get_product_snapshot(self, obj):
        order = obj.order
        items_count = order.order_items.count()

        if items_count == 0:
            return None
        elif items_count == 1:
            item = order.order_items.first()
            return {
                'name': item.product.title,
                'count': 1
            }
        else:
            return {
                'name': '多件商品',
                'count': items_count
            }


class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'type', 'type_display', 'title', 'content',
                  'read', 'created_at', 'related_id', 'related_data']
        read_only_fields = ['id', 'created_at']


class SecurityPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPolicy
        fields = ['policy_id', 'policy_name', 'policy_description',
                  'is_enabled', 'security_level', 'created_at', 'updated_at']
        read_only_fields = ['policy_id', 'created_at', 'updated_at']
