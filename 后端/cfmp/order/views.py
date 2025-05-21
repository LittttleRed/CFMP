from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
    UpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Sum, Q
from .models import Order, OrderItem, Payment, Notification, SecurityPolicy
from .serializers import (
    OrderSerializer, OrderListSerializer, CreateOrderSerializer,
    PaymentSerializer, PaymentListSerializer, CreatePaymentSerializer,
    NotificationSerializer, SecurityPolicySerializer
)
import uuid
import json

# 自定义分页类
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# 订单相关视图
class OrderListCreateAPIView(ListCreateAPIView):
    """获取订单列表或创建新订单"""
    serializer_class = OrderListSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """根据状态筛选订单"""
        user = self.request.user
        status_filter = self.request.query_params.get('status')

        queryset = Order.objects.filter(buyer=user)

        if status_filter and status_filter != 'all':
            status_map = {
                'pending_payment': 0,
                'paid': 1,
                'completed': 2,
                'cancelled': 3
            }
            if status_filter in status_map:
                queryset = queryset.filter(status=status_map[status_filter])

        # 处理排序
        sort = self.request.query_params.get('sort', 'created_desc')
        if sort == 'created_desc':
            queryset = queryset.order_by('-created_at')
        elif sort == 'created_asc':
            queryset = queryset.order_by('created_at')
        elif sort == 'amount_desc':
            queryset = queryset.order_by('-total_amount')
        elif sort == 'amount_asc':
            queryset = queryset.order_by('total_amount')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 创建订单
        order = serializer.save()

        # 返回响应
        return Response({
            'code': 200,
            'data': {
                'order_id': order.order_id,
                'status': 'pending_payment',
                'created_at': order.created_at,
                'total_amount': order.total_amount,
                'payment_url': f'/api/payment/create?order_id={order.order_id}'
            }
        }, status=status.HTTP_201_CREATED)

class OrderDetailAPIView(RetrieveAPIView):
    """获取订单详情"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'data': serializer.data
        })

class OrderCancelAPIView(UpdateAPIView):
    """取消订单"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user, status=0)  # 只能取消待支付的订单

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # 更新订单状态为已取消
        order.status = 3
        order.cancel_reason = request.data.get('reason', '')
        order.save()

        return Response({
            'code': 200,
            'message': '订单已成功取消',
            'data': {
                'success': True,
                'order_id': order.order_id,
                'current_status': 'cancelled'
            }
        })

class OrderCompleteAPIView(UpdateAPIView):
    """确认收货完成订单"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user, status=1)  # 只能确认已支付的订单

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # 更新订单状态为已完成
        order.status = 2
        order.save()

        # 创建一个通知
        Notification.objects.create(
            user=order.buyer,
            type=0,  # 交易通知
            title='订单已完成',
            content=f'您的订单#{order.order_id}已成功完成，感谢您的购买!',
            related_id=str(order.order_id)
        )

        return Response({
            'code': 200,
            'message': '订单已成功确认完成',
            'data': {
                'success': True,
                'order_id': order.order_id,
                'current_status': 'completed'
            }
        })

class OrderStatsAPIView(APIView):
    """获取订单状态统计"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 获取用户的所有订单
        orders = Order.objects.filter(buyer=user)
        total = orders.count()

        # 按状态统计
        pending_payment = orders.filter(status=0).count()
        paid = orders.filter(status=1).count()
        completed = orders.filter(status=2).count()
        cancelled = orders.filter(status=3).count()

        return Response({
            'code': 200,
            'data': {
                'total': total,
                'pending_payment': pending_payment,
                'paid': paid,
                'completed': completed,
                'cancelled': cancelled
            }
        })

# 支付相关视图
class PaymentCreateAPIView(APIView):
    """创建支付请求"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 获取参数
        order_id = request.query_params.get('order_id')
        total_amount = request.query_params.get('total_amount')
        payment_method = request.query_params.get('payment_method')
        payment_subject = request.query_params.get('payment_subject')
        return_url = request.query_params.get('return_url')

        # 验证参数
        if not all([order_id, total_amount, payment_method, payment_subject]):
            return Response({
                'code': 400,
                'message': '参数不完整'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取订单信息
        try:
            order = Order.objects.get(order_id=order_id, buyer=request.user)
        except Order.DoesNotExist:
            return Response({
                'code': 404,
                'message': '订单不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 判断订单状态
        if order.status != 0:
            return Response({
                'code': 400,
                'message': '该订单状态不允许支付'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 生成支付ID
        payment_id = f"PAY{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4().int)[:4]}"

        # 支付方式映射
        payment_method_map = {
            'alipay': 0,
            'wechat_pay': 1
        }

        # 创建支付记录
        payment = Payment.objects.create(
            payment_id=payment_id,
            order=order,
            user=request.user,
            amount=total_amount,
            payment_method=payment_method_map.get(payment_method, 0),
            payment_subject=payment_subject,
            expires_at=timezone.now() + timezone.timedelta(minutes=30)
        )

        # TODO:这里的可能并不能真的到达支付宝，需要依据支付宝的接口规则进行更改
        # 根据支付方式准备支付数据
        payment_data = {}
        if payment_method == 'alipay':
            payment_data = {
                'url': f"https://openapi.alipay.com/gateway.do?order_id={order_id}&payment_id={payment_id}"
            }
        elif payment_method == 'wechat_pay':
            payment_data = {
                'url': f"https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?order_id={order_id}&payment_id={payment_id}",
                'qrcode': f"weixin://wxpay/bizpayurl?pr={payment_id}"
            }

        # 更新支付数据
        payment.payment_data = payment_data
        payment.save()

        return Response({
            'code': 200,
            'message': '支付请求创建成功',
            'data': {
                'payment_type': payment_method,
                'payment_id': payment_id,
                'order_id': order_id,
                'payment_data': payment_data,
                'expires_at': payment.expires_at
            }
        })

class PaymentCallbackAPIView(APIView):
    """支付回调处理"""
    def get(self, request, payment_method):
        """同步回调"""
        # 处理回调参数
        order_id = request.query_params.get('order_id')
        status_param = request.query_params.get('status')

        return Response("success")

    def post(self, request, payment_method):
        """异步回调"""
        # 解析回调参数
        trade_no = request.query_params.get('trade_no')
        out_trade_no = request.query_params.get('out_trade_no')
        order_id = request.query_params.get('order_id')
        status_param = request.query_params.get('status')
        total_amount = request.query_params.get('total_amount')
        sign = request.query_params.get('sign')

        # 实际应用中需要验证签名

        # 假设支付已成功
        try:
            payment = Payment.objects.get(payment_id=out_trade_no)
            order = payment.order

            # 更新支付状态
            payment.status = 2  # 成功
            payment.transaction_id = trade_no
            payment.paid_at = timezone.now()
            payment.save()

            # 更新订单状态
            order.status = 1  # 已支付
            order.payment_time = timezone.now()
            order.save()

            # 创建通知
            Notification.objects.create(
                user=order.buyer,
                type=0,  # 交易通知
                title='支付成功通知',
                content=f'您的订单 #{order.order_id} 已成功支付，感谢您的购买！',
                related_id=str(order.order_id),
                related_data={
                    'order_id': str(order.order_id),
                    'payment_amount': float(payment.amount),
                    'payment_method': payment.get_payment_method_display()
                }
            )

        except (Payment.DoesNotExist, Order.DoesNotExist):
            return Response({
                'status': 'failed',
                'message': '找不到对应的支付记录或订单'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'status': 'success',
            'message': '回调成功处理'
        })

class PaymentQueryAPIView(RetrieveAPIView):
    """支付查询"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, buyer=request.user)
        except Order.DoesNotExist:
            return Response({
                'code': 404,
                'message': '订单不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            payment = Payment.objects.get(order=order)
        except Payment.DoesNotExist:
            return Response({
                'code': 404,
                'message': '支付记录不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 获取订单商品
        products = []
        for item in order.order_items.all():
            products.append({
                'product_id': item.product.product_id,
                'name': item.product.title,
                'price': float(item.price),
                'quantity': item.quantity
            })

        # 构建响应数据
        data = {
            'order_id': str(order.order_id),
            'payment_id': payment.payment_id,
            'status': payment.get_status_display(),
            'payment_method': payment.get_payment_method_display(),
            'created_at': payment.created_at,
            'amount': float(payment.amount),
            'products': products
        }

        # 根据支付状态添加不同字段
        if payment.status == 2:  # 支付成功
            data['paid_at'] = payment.paid_at
            data['transaction_id'] = payment.transaction_id
        elif payment.status == 3:  # 支付失败
            data['failure_reason'] = payment.failure_reason

        return Response({
            'code': 200,
            'data': data
        })

class PaymentRecordsAPIView(ListAPIView):
    """获取支付记录列表"""
    serializer_class = PaymentListSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status')

        queryset = Payment.objects.filter(user=user)

        # 按状态筛选
        if status_filter and status_filter != 'all':
            status_map = {
                'pending': 0,
                'success': 2,
                'failed': 3
            }
            if status_filter in status_map:
                queryset = queryset.filter(status=status_map[status_filter])

        # 处理排序
        sort = self.request.query_params.get('sort', 'created_desc')
        if sort == 'created_desc':
            queryset = queryset.order_by('-created_at')
        elif sort == 'created_asc':
            queryset = queryset.order_by('created_at')
        elif sort == 'amount_desc':
            queryset = queryset.order_by('-amount')
        elif sort == 'amount_asc':
            queryset = queryset.order_by('amount')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'data': {
                    'total': self.paginator.page.paginator.count,
                    'page': self.paginator.page.number,
                    'page_size': self.paginator.page_size,
                    'records': serializer.data
                }
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'data': {
                'total': queryset.count(),
                'page': 1,
                'page_size': len(queryset),
                'records': serializer.data
            }
        })

class PaymentCancelAPIView(APIView):
    """取消支付"""
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({
                'code': 404,
                'message': '支付记录不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 检查支付状态是否可取消
        if payment.status not in [0, 1]:  # 待支付或处理中
            return Response({
                'code': 400,
                'message': '当前支付状态不可取消'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新支付状态为已取消
        payment.status = 4
        payment.save()

        return Response({
            'code': 200,
            'message': '支付已取消',
            'data': {
                'success': True,
                'payment_id': payment.payment_id,
                'order_id': str(payment.order.order_id),
                'status': 'cancelled'
            }
        })

# 通知相关视图
class NotificationListAPIView(ListAPIView):
    """获取通知列表"""
    serializer_class = NotificationSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        type_filter = self.request.query_params.get('type')
        unread_only = self.request.query_params.get('unread_only')

        queryset = Notification.objects.filter(user=user)

        # 按类型筛选
        if type_filter in ['transaction', 'system', 'promotion']:
            type_map = {
                'transaction': 0,
                'system': 1,
                'promotion': 2
            }
            queryset = queryset.filter(type=type_map[type_filter])

        # 只返回未读通知
        if unread_only and unread_only.lower() == 'true':
            queryset = queryset.filter(read=False)

        # 按时间倒序排序
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 获取未读数量
        unread_count = queryset.filter(read=False).count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'data': {
                    'total': self.paginator.page.paginator.count,
                    'page': self.paginator.page.number,
                    'page_size': self.paginator.page_size,
                    'unread_count': unread_count,
                    'notifications': serializer.data
                }
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'data': {
                'total': queryset.count(),
                'page': 1,
                'page_size': len(queryset),
                'unread_count': unread_count,
                'notifications': serializer.data
            }
        })

class NotificationDetailAPIView(RetrieveAPIView):
    """获取通知详情"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 标记为已读
        if not instance.read:
            instance.read = True
            instance.save()

        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'data': serializer.data
        })

class NotificationDeleteAPIView(APIView):
    """删除通知"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return Response({
                'code': 404,
                'message': '通知不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        notification.delete()

        return Response({
            'code': 200,
            'message': '通知已删除',
            'data': {
                'success': True,
                'notification_id': notification_id
            }
        })

class NotificationMarkReadAPIView(APIView):
    """标记通知为已读"""
    permission_classes = [IsAuthenticated]

    def put(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return Response({
                'code': 404,
                'message': '通知不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        notification.read = True
        notification.save()

        return Response({
            'code': 200,
            'message': '通知已标记为已读',
            'data': {
                'success': True,
                'notification_id': notification_id
            }
        })

class NotificationMarkAllReadAPIView(APIView):
    """全部标记为已读"""
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        type_filter = request.query_params.get('type')

        queryset = Notification.objects.filter(user=user, read=False)

        # 按类型筛选
        if type_filter in ['transaction', 'system', 'promotion']:
            type_map = {
                'transaction': 0,
                'system': 1,
                'promotion': 2
            }
            queryset = queryset.filter(type=type_map[type_filter])

        # 更新为已读
        count = queryset.count()
        queryset.update(read=True)

        return Response({
            'code': 200,
            'message': '所有通知已标记为已读',
            'data': {
                'success': True,
                'count': count
            }
        })

class NotificationUnreadCountAPIView(APIView):
    """获取未读通知数量"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        type_filter = request.query_params.get('type')

        # 获取所有未读通知
        queryset = Notification.objects.filter(user=user, read=False)

        # 如果指定了类型，就只计算该类型的
        if type_filter in ['transaction', 'system', 'promotion']:
            type_map = {
                'transaction': 0,
                'system': 1,
                'promotion': 2
            }
            queryset = queryset.filter(type=type_map[type_filter])

        # 总未读数量
        total_unread = queryset.count()

        # 按类型统计未读数量
        by_type = {
            'transaction': queryset.filter(type=0).count(),
            'system': queryset.filter(type=1).count(),
            'promotion': queryset.filter(type=2).count()
        }

        return Response({
            'code': 200,
            'data': {
                'total_unread': total_unread,
                'by_type': by_type
            }
        })

# 安全策略相关视图
class RiskAssessmentAPIView(APIView):
    """风险评估"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 简化实现，实际中需根据多种因素计算风险

        # 模拟风险评估结果
        risk_level = "medium"
        risk_factors = [
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
        ]

        return Response({
            'code': 200,
            'data': {
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendation': "建议进行二次身份验证"
            }
        })

class FraudDetectionAPIView(APIView):
    """欺诈检测"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 简化实现，实际中需要复杂的欺诈检测算法

        # 模拟欺诈检测结果
        fraud_score = 75
        fraud_detected = True
        fraud_types = ["identity_theft", "unusual_behavior"]

        return Response({
            'code': 200,
            'data': {
                'fraud_score': fraud_score,
                'fraud_detected': fraud_detected,
                'fraud_types': fraud_types,
                'action_recommended': "review"
            }
        })

class SecurityPolicyListAPIView(APIView):
    """获取安全策略配置"""

    def get(self, request):
        # 获取所有启用的安全策略
        policies = SecurityPolicy.objects.all()

        # 序列化策略数据
        serializer = SecurityPolicySerializer(policies, many=True)

        # 确定整体安全级别
        high_count = policies.filter(security_level='high', is_enabled=True).count()
        medium_count = policies.filter(security_level='medium', is_enabled=True).count()

        if high_count > 1:
            security_level = 'high'
        elif medium_count > 2:
            security_level = 'medium'
        else:
            security_level = 'low'

        return Response({
            'code': 200,
            'data': {
                'security_level': security_level,
                'policies': serializer.data
            }
        })

class SecurityPolicyUpdateAPIView(APIView):
    """更新安全策略配置"""
    permission_classes = [IsAdminUser]  # 只有管理员可以更新

    def put(self, request):
        data = request.data
        security_level = data.get('security_level', 'medium')
        policies = data.get('policies', [])

        # 更新策略
        for policy_data in policies:
            policy_id = policy_data.get('policy_id')
            is_enabled = policy_data.get('is_enabled')

            if policy_id and is_enabled is not None:
                try:
                    policy = SecurityPolicy.objects.get(policy_id=policy_id)
                    policy.is_enabled = is_enabled
                    policy.save()
                except SecurityPolicy.DoesNotExist:
                    pass

        return Response({
            'code': 200,
            'message': '安全策略更新成功',
            'data': {
                'updated': True,
                'security_level': security_level
            }
        })
