from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from model import models
from model import serializers
from rest_framework.views import APIView


@api_view(['PUT'])
def admin_user_get(request):
    return Response({'code': "200", 'message': 'admin_user_get'})


# Create your views here.


# 基于函数的视图
@api_view(['GET', 'POST'])
def test(request, test_int):
    print(request.path)  # 去掉域名的路径
    print(request.method)  # 请求方法
    print(request.query_params.dict())  # query形式的参数,转化为字典,DRF专属
    print(request.data)  # json形式的参数,存在请求体中,纯字典形式
    print(request.headers)  # 请求头内容
    print(test_int)
    # 序列化并返回结果

    # 签名Response(data, status=None, template_name=None, headers=None, content_type=None)
    """
    data:返回的数据，内部会进行序列化，需传入一个字典
    status:状态码,默认是200
    header:响应头
    """
    return Response({'code': "200", 'message': 'test'}, status=200, headers={'Content-Type': 'application/json'})


class TestView(APIView):
    """
    基于类的视图
    """

    def get(self, request):
        return Response({'code': "123213", 'message': 'test'}, status=200, headers={'Content-Type': 'application/json'})

    def post(self, request):
        return Response({'code': "123213", 'message': 'testpost'}, status=200,
                        headers={'Content-Type': 'application/json'})

    def patch(self, request):
        return Response({'code': "123213", 'message': 'testpatch'}, status=200,
                        headers={'Content-Type': 'application/json'})


class TestGenericView(GenericAPIView):
    queryset = models.TransactionLog.objects.all()
    serializer_class = serializers.TransactionLogSerializer
    #lookup_field = 'id'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': "200", 'message': 'create success'})
