from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..model import models
@api_view(['PUT'])
def admin_user_get(request):
    return Response({'code': "200", 'message':'admin_user_get'})
# Create your views here.
def test(request):
    params = request.query_params.dict()

    # 初始化查询集
    queryset = models.User.objects.all()

    # 动态过滤（自动匹配模型字段）
    if params:
        # 过滤参数需要是模型的字段
        valid_fields = [f.name for f in models.User._meta.get_fields()]
        filtered_params = {k: v for k, v in params.items() if k in valid_fields}

        # 使用 ** 解包参数进行过滤
        queryset = queryset.filter(**filtered_params)

    # 序列化并返回结果
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)