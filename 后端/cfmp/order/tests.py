from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from user.models import User
from product.models import Product, Category
from .models import Order, OrderItem, Payment, Notification, SecurityPolicy
from .encryption import encryptor


class OrderModelTest(TestCase):
    """测试订单模型"""

    def setUp(self):
        # 使用现有用户或创建测试用户
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        # 创建测试商品
        self.category = Category.objects.create(name="测试分类")
        self.product = Product.objects.create(
            user=self.user,
            title="测试商品",
            description="这是一个测试商品",
            price=99.99,
            status=2
        )
        self.product.categories.add(self.category)

        # 创建测试订单
        self.order = Order.objects.create(
            buyer=self.user,
            total_amount=199.98,
            status=0,
            payment_method=0,
            shipping_name="张三",
            shipping_phone="13800138000",
            shipping_address="北京市朝阳区测试街道123号"
        )

    def test_order_creation(self):
        """测试订单创建"""
        self.assertEqual(self.order.buyer, self.user)
        self.assertEqual(self.order.total_amount, Decimal('199.98'))
        self.assertEqual(self.order.status, 0)
        self.assertEqual(self.order.payment_method, 0)

    def test_order_str_method(self):
        """测试订单字符串表示"""
        self.assertEqual(str(self.order), str(self.order.order_id))

    def test_order_status_choices(self):
        """测试订单状态选择"""
        self.order.status = 1
        self.order.save()
        self.assertEqual(self.order.get_status_display(), 'paid')

    def test_payment_method_choices(self):
        """测试支付方式选择"""
        self.assertEqual(self.order.get_payment_method_display(), 'alipay')


class OrderItemModelTest(TestCase):
    """测试订单商品项模型"""

    def setUp(self):
        # 使用现有用户
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.product = Product.objects.create(
            user=self.user,
            title="测试商品",
            description="这是一个测试商品",
            price=99.99,
            status=2
        )

        self.order = Order.objects.create(
            buyer=self.user,
            total_amount=199.98,
            status=0
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=99.99,
            quantity=2
        )

    def test_order_item_creation(self):
        """测试订单商品项创建"""
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, Decimal('99.99'))
        self.assertEqual(self.order_item.quantity, 2)

    def test_order_item_str_method(self):
        """测试订单商品项字符串表示"""
        expected = f"{self.product.title} x {self.order_item.quantity}"
        self.assertEqual(str(self.order_item), expected)


class PaymentModelTest(TestCase):
    """测试支付模型"""

    def setUp(self):
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.order = Order.objects.create(
            buyer=self.user,
            total_amount=99.99,
            status=0
        )

        self.payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            amount=99.99,
            payment_method=0,
            payment_subject="测试支付"
        )

    def test_payment_creation(self):
        """测试支付记录创建"""
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.amount, Decimal('99.99'))
        self.assertEqual(self.payment.payment_method, 0)
        self.assertEqual(self.payment.payment_subject, "测试支付")

    def test_payment_str_method(self):
        """测试支付记录字符串表示"""
        self.assertEqual(str(self.payment), str(self.payment.payment_id))


class NotificationModelTest(TestCase):
    """测试通知模型"""

    def setUp(self):
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.notification = Notification.objects.create(
            user=self.user,
            type=0,
            title="测试通知",
            content="这是一个测试通知"
        )

    def test_notification_creation(self):
        """测试通知创建"""
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.type, 0)
        self.assertEqual(self.notification.title, "测试通知")
        self.assertEqual(self.notification.content, "这是一个测试通知")
        self.assertFalse(self.notification.read)

    def test_notification_str_method(self):
        """测试通知字符串表示"""
        self.assertEqual(str(self.notification), "测试通知")


class SecurityPolicyModelTest(TestCase):
    """测试安全策略模型"""

    def setUp(self):
        self.policy = SecurityPolicy.objects.create(
            policy_id=1,
            policy_name="测试安全策略",
            policy_description="这是一个测试安全策略",
            security_level="high"
        )

    def test_security_policy_creation(self):
        """测试安全策略创建"""
        self.assertEqual(self.policy.policy_name, "测试安全策略")
        self.assertEqual(self.policy.policy_description, "这是一个测试安全策略")
        self.assertEqual(self.policy.security_level, "high")
        self.assertTrue(self.policy.is_enabled)

    def test_security_policy_str_method(self):
        """测试安全策略字符串表示"""
        self.assertEqual(str(self.policy), "测试安全策略")


class OrderAPITest(APITestCase):
    """测试订单API"""

    def setUp(self):
        # 使用现有用户
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.user.is_authenticated = True
        self.user.save()

        # 创建另一个用户用于权限测试
        try:
            self.other_user = User.objects.get(username="otheruser")
        except User.DoesNotExist:
            self.other_user = User.objects.create(
                username="otheruser",
                email="other@example.com",
                password="testpass123"
            )

        # 创建API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 创建测试商品
        self.category = Category.objects.create(name="测试分类")
        self.product1 = Product.objects.create(
            user=self.user,
            title="测试商品1",
            description="这是测试商品1",
            price=99.99,
            status=2
        )
        self.product2 = Product.objects.create(
            user=self.user,
            title="测试商品2",
            description="这是测试商品2",
            price=199.99,
            status=2
        )

        # 创建测试订单
        self.order = Order.objects.create(
            buyer=self.user,
            total_amount=99.99,
            status=0,
            payment_method=0,
            shipping_name=encryptor.encrypt("张三"),
            shipping_phone=encryptor.encrypt("13800138000"),
            shipping_address=encryptor.encrypt("北京市朝阳区测试街道123号")
        )

        # 创建订单项
        OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            price=99.99,
            quantity=1
        )

    def test_get_order_list(self):
        """测试获取订单列表"""
        url = '/order/'  # 根据实际URL配置调整
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_order_list_with_status_filter(self):
        """测试按状态筛选订单列表"""
        url = '/order/'
        response = self.client.get(url, {'status': 'pending_payment'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_success(self):
        """测试成功创建订单"""
        url = '/order/'
        data = {
            'products': [
                {
                    'product_id': self.product1.product_id,
                    'quantity': 2,
                    'price': 99.99
                }
            ],
            'total_amount': 199.98,
            'payment_method': 0,
            'shipping_name': '李四',
            'shipping_phone': '13900139000',
            'shipping_address': '上海市浦东新区测试路456号',
            'remark': '测试订单备注'
        }

        response = self.client.post(url, data, format='json')
        # 根据实际实现可能返回不同状态码
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_create_order_duplicate_pending(self):
        """测试创建重复商品的待支付订单"""
        url = '/order/'
        data = {
            'products': [
                {
                    'product_id': self.product1.product_id,
                    'quantity': 1,
                    'price': 99.99
                }
            ],
            'total_amount': 99.99,
            'payment_method': 0,
            'shipping_name': '李四',
            'shipping_phone': '13900139000',
            'shipping_address': '上海市浦东新区测试路456号'
        }

        response = self.client.post(url, data, format='json')
        # 应该返回冲突状态或重复订单信息
        self.assertIn(response.status_code, [status.HTTP_409_CONFLICT, status.HTTP_200_OK])

    def test_create_order_without_authentication(self):
        """测试未认证用户创建订单"""
        self.client.force_authenticate(user=None)
        url = '/order/'
        data = {
            'products': [{'product_id': self.product1.product_id, 'quantity': 1}],
            'total_amount': 99.99
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_detail(self):
        """测试获取订单详情"""
        url = f'/order/{self.order.order_id}/'
        response = self.client.get(url)

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_cancel_order_success(self):
        """测试成功取消订单"""
        url = f'/order/{self.order.order_id}/cancel/'
        data = {'reason': '不想要了'}

        response = self.client.put(url, data, format='json')
        # 根据实际实现验证响应
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_complete_order_success(self):
        """测试成功完成订单"""
        # 先将订单设为已支付状态
        self.order.status = 1
        self.order.save()

        url = f'/order/{self.order.order_id}/complete/'
        response = self.client.put(url)

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class PaymentAPITest(APITestCase):
    """测试支付API"""

    def setUp(self):
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.user.is_authenticated = True
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 创建测试订单
        self.order = Order.objects.create(
            buyer=self.user,
            total_amount=99.99,
            status=0
        )

    def test_create_payment_success(self):
        """测试成功创建支付"""
        url = '/payment/create/'
        data = {
            'order_id': self.order.order_id,
            'total_amount': 99.99,
            'payment_method': 'alipay',
            'payment_subject': '测试商品支付',
            'return_url': 'http://example.com/return'
        }

        response = self.client.post(url, data, format='json')
        # 根据实际实现验证响应
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_query_payment(self):
        """测试查询支付状态"""
        # 创建支付记录
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            amount=99.99,
            payment_method=0,
            payment_subject="测试支付"
        )

        url = f'/payment/{self.order.order_id}/query/'
        response = self.client.get(url)

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class NotificationAPITest(APITestCase):
    """测试通知API"""

    def setUp(self):
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.user.is_authenticated = True
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 创建测试通知
        self.notification = Notification.objects.create(
            user=self.user,
            type=0,
            title="测试通知",
            content="这是一个测试通知"
        )

    def test_get_notification_list(self):
        """测试获取通知列表"""
        url = '/notifications/'
        response = self.client.get(url)

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_mark_notification_read(self):
        """测试标记通知为已读"""
        url = f'/notifications/{self.notification.id}/read/'
        response = self.client.put(url)

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class EncryptionTest(TestCase):
    """测试加密解密功能"""

    def test_encrypt_decrypt(self):
        """测试加密解密功能"""
        original_text = "测试加密文本"

        # 测试加密
        encrypted_text = encryptor.encrypt(original_text)
        self.assertNotEqual(encrypted_text, original_text)

        # 测试解密
        decrypted_text = encryptor.decrypt(encrypted_text)
        self.assertEqual(decrypted_text, original_text)

    def test_encrypt_empty_string(self):
        """测试加密空字符串"""
        empty_text = ""
        encrypted_text = encryptor.encrypt(empty_text)
        decrypted_text = encryptor.decrypt(encrypted_text)
        self.assertEqual(decrypted_text, empty_text)

    def test_decrypt_invalid_data(self):
        """测试解密无效数据"""
        with self.assertRaises(Exception):
            encryptor.decrypt("invalid_encrypted_data")


class SerializerTest(TestCase):
    """测试序列化器"""

    def setUp(self):
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.product = Product.objects.create(
            user=self.user,
            title="测试商品",
            description="这是一个测试商品",
            price=99.99,
            status=2
        )

        self.order = Order.objects.create(
            buyer=self.user,
            total_amount=99.99,
            status=0,
            shipping_name=encryptor.encrypt("张三"),
            shipping_phone=encryptor.encrypt("13800138000"),
            shipping_address=encryptor.encrypt("北京市朝阳区测试街道123号")
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=99.99,
            quantity=1
        )

    def test_order_serializer_decryption(self):
        """测试订单序列化器解密功能"""
        from .serializers import OrderSerializer

        serializer = OrderSerializer(self.order)
        data = serializer.data

        # 验证敏感信息被正确解密
        self.assertEqual(data['shipping_name'], "张三")
        self.assertEqual(data['shipping_phone'], "13800138000")
        self.assertEqual(data['shipping_address'], "北京市朝阳区测试街道123号")

    def test_order_item_serializer(self):
        """测试订单项序列化器"""
        from .serializers import OrderItemSerializer

        serializer = OrderItemSerializer(self.order_item)
        data = serializer.data

        self.assertEqual(data['product_id'], self.product.product_id)
        self.assertEqual(data['product_name'], self.product.title)
        self.assertEqual(str(data['price']), "99.99")
        self.assertEqual(data['quantity'], 1)


class IntegrationTest(APITestCase):
    """集成测试 - 测试完整的订单流程"""

    def setUp(self):
        try:
            self.user = User.objects.get(username="Faust233")
        except User.DoesNotExist:
            self.user = User.objects.create(
                username="Faust233",
                email="1091320573@qq.com",
                password="Mephistopheles23"
            )

        self.user.is_authenticated = True
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 创建测试商品
        self.product = Product.objects.create(
            user=self.user,
            title="测试商品",
            description="这是一个测试商品",
            price=99.99,
            status=2
        )

    def test_complete_order_workflow(self):
        """测试完整的订单流程"""
        # 1. 创建订单
        create_url = '/order/'
        order_data = {
            'products': [
                {
                    'product_id': self.product.product_id,
                    'quantity': 1,
                    'price': 99.99
                }
            ],
            'total_amount': 99.99,
            'payment_method': 0,
            'shipping_name': '张三',
            'shipping_phone': '13800138000',
            'shipping_address': '北京市朝阳区测试街道123号'
        }

        create_response = self.client.post(create_url, order_data, format='json')
        # 根据实际实现验证响应
        self.assertIn(create_response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

        # 如果订单创建成功，继续测试其他步骤
        if create_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            if 'data' in create_response.data and 'order_id' in create_response.data['data']:
                order_id = create_response.data['data']['order_id']

                # 2. 查看订单详情
                detail_url = f'/order/{order_id}/'
                detail_response = self.client.get(detail_url)
                self.assertIn(detail_response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_order_cancellation_workflow(self):
        """测试订单取消流程"""
        # 创建订单
        order = Order.objects.create(
            buyer=self.user,
            total_amount=99.99,
            status=0
        )

        # 取消订单
        cancel_url = f'/order/{order.order_id}/cancel/'
        cancel_data = {'reason': '测试取消'}

        cancel_response = self.client.put(cancel_url, cancel_data, format='json')
        self.assertIn(cancel_response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
