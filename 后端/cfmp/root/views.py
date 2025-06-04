from datetime import timezone, timedelta, datetime

import django_filters
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework import generics, mixins, viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from . import serializers
from rest_framework.views import APIView
from . import filter
from user.models import Messages,User
from .permissions import IsAdminUser
from product.models import Product

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class StandartView(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        list = super().list(request, *args, **kwargs)
        return Response({'data': list.data})

    def retrieve(self, request, *args, **kwargs):#带路径参数的查询
        retrieve = super().retrieve(request, *args, **kwargs)
        return Response({'data': retrieve.data})

    def create(self, request, *args, **kwargs):
        create = super().create(request, *args, **kwargs)
        return Response({'data': create.data})

    def update(self, request, *args, **kwargs):
        update = super().update(request, *args, **kwargs)
        return Response({'data': update.data})


@api_view(['PUT'])
def admin_user_get(request):
    return Response({'code': "200", 'message': 'admin_user_get'})


# Create your views here.
class UserView(StandartView):
    permission_classes = [IsAdminUser]

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'user_id'
    pagination_class = StandardPagination

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['user_id','username','status','privilege']
    ordering_fields = ['created_at']

class ProductView(StandartView):
    permission_classes = [IsAdminUser]

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'product_id'
    pagination_class = StandardPagination

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at']


class ComplaintView(StandartView):
    permission_classes = [IsAdminUser]
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    lookup_field = 'complaint_id'
    pagination_class = StandardPagination


    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['complainer_id','target_id','target_type','status','complainer_id']
    ordering_fields = ['created_at']

    @action(methods=['patch'], detail=False, url_path='branch/(?P<target_type>\w+)/(?P<target_id>\d+)', url_name='branch')
    def branch_update(self, request,target_type, target_id):
        queryset = self.get_queryset().filter(
            target_type=target_type,
            target_id=target_id
        )
        if not queryset.exists():
            return Response({'detail':'没有对应的举报'},status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer()
        for complaint in queryset:
            serializer = self.get_serializer(complaint, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

        return Response(status=status.HTTP_202_ACCEPTED)


#增加过滤器
# class ComplaintReviewFilter(django_filters.FilterSet):
#     #获取特定物品对应举报的举报记录
#     target_id = django_filters.NumberFilter(field_name='complaint_id__target_id')
#     target_type = django_filters.NumberFilter(field_name='complaint_id__target_type')
#     class Meta:
#         model = models.ComplaintReview
#         fields = ['target_id', 'target_type']


class ComplaintReviewView(StandartView):
    permission_classes = [IsAdminUser]
    queryset = models.ComplaintReview.objects.all()
    serializer_class = serializers.ComplaintReviewSerializer
    lookup_field = 'review_id'
    pagination_class = StandardPagination

    # filter_class = ComplaintReviewFilter
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['target_id', 'target_type','reviewer_id']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        # 调用父类的 create 方法完成数据的创建
        response = super().create(request, *args, **kwargs)

        # 获取当前创建的投诉审核数据
        target_id = request.data.get('target_id')
        target_type = request.data.get('target_type')


        # 查询所有举报了该 target_type 和 target_id 的用户
        complaints = models.Complaint.objects.filter(target_id=target_id, target_type=target_type,status=0)
        complainer_ids = complaints.values_list('complainer_id', flat=True).distinct()

        # 获取对应的用户对象列表
        users = User.objects.filter(user_id__in=complainer_ids)

        # 创建消息并关联到用户
        message_title = "举报处理通知"
        message_type = ""
        if target_type == 0:
            message_type = "product"
        elif target_type == 1:
            message_type = "user"
        message_content = f"您举报的目标 (ID: {target_id}, 类型: {message_type}) 已经有了新的处理结果，请及时查看。"
        message = Messages.objects.create(title=message_title, content=message_content)

        for user in users:
            user.messages.add(message)  # 将消息关联到用户

        # 返回原始响应数据
        return response

#解封定时任务


class OrderView(StandartView):
    permission_classes = [IsAdminUser]
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filterset_class = filter.OrderFilter
    lookup_field = 'order_id'
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['status']

