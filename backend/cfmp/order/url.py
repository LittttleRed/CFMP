from django.urls import path
from . import views

urlpatterns = [
    # 订单相关路由
    path('orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:order_id>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/cancel/', views.OrderCancelAPIView.as_view(), name='order-cancel'),
    path('orders/<int:order_id>/complete/', views.OrderCompleteAPIView.as_view(), name='order-complete'),
    path('orders/stats/', views.OrderStatsAPIView.as_view(), name='order-stats'),

    # 支付相关路由
    path('payment/create/', views.PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/callback/<str:payment_method>/', views.PaymentCallbackAPIView.as_view(), name='payment-callback'),
    path('payment/<int:order_id>/', views.PaymentQueryAPIView.as_view(), name='payment-query'),
    path('payment/records/', views.PaymentRecordsAPIView.as_view(), name='payment-records'),
    path('payment/<str:payment_id>/cancel/', views.PaymentCancelAPIView.as_view(), name='payment-cancel'),    # 通知相关路由
    path('notifications/', views.NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/', views.NotificationDeleteAPIView.as_view(), name='notification-delete'),
    path('notifications/<int:notification_id>/read/', views.NotificationMarkReadAPIView.as_view(), name='notification-mark-read'),
    path('notifications/read-all/', views.NotificationMarkAllReadAPIView.as_view(), name='notification-read-all'),
    path('notifications/unread-count/', views.NotificationUnreadCountAPIView.as_view(), name='notification-unread-count'),
    path('notifications/detail/<int:id>/', views.NotificationDetailAPIView.as_view(), name='notification-detail'),

    # 安全策略相关路由
    path('security/risk-assessment/', views.RiskAssessmentAPIView.as_view(), name='security-risk-assessment'),
    path('security/fraud-detection/', views.FraudDetectionAPIView.as_view(), name='security-fraud-detection'),
    path('security/policies/', views.SecurityPolicyListAPIView.as_view(), name='security-policies-list'),
    path('security/policies/update/', views.SecurityPolicyUpdateAPIView.as_view(), name='security-policies-update'),
]

