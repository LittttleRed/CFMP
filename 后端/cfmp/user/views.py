import urllib3
import jwt
import datetime
from datetime import datetime, timedelta, timezone
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.contrib.auth import authenticate
from minio_storage import MinioMediaStorage
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import UserSerializer, PublicUserSerializer
from .models import User
from minio import Minio
from django.conf import settings
from jwt import exceptions
# Create your views here.





class login(APIView):
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([email, password]):
            return Response({
                "fail_code":"MISSING_PARAM",
                "fail_msg":"邮箱和密码不能为空"
            },status=status.HTTP_400_BAD_REQUEST)

        # user = authenticate(email=email, password=password)
        user = User.objects.filter(email=email,password=password)
        # 反序列化user
        user = user.first()
        print(user)
        if user:
            salt = settings.SECRET_KEY
            headers = {
                'typ':'jwt',
                'alg':'HS256'
            }
            print(user.username)
            payload = {
                'user_id': user.user_id,
                'username': user.username,
                'exp':datetime.now(timezone.utc) + timedelta(days=3)  # 延长token有效期为60分钟
            }

            token = jwt.encode(payload = payload, key = salt, algorithm="HS256", headers=headers)

            return Response({
                "success":True,
                "access_token":token,
                "username":user.username,
                "user_id":user.user_id,
            })

        try:
            User.objects.get(email=email)
            return Response({
                "success": False,
                "fail_code": "WRONG_PASSWORD",
                "fail_msg": "账密错误"
            }, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "fail_code": "USER_NOT_FOUND",
                "fail_msg": "用户不存在"
            }, status=status.HTTP_404_NOT_FOUND)

class UserIdViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    lookup_field = 'user_id'

class UserInfoView(ListCreateAPIView,RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 直接返回当前请求的用户对象（通过 Token 解析出的用户）
        return self.request.user
    def get_queryset(self):
        return User.objects.filter(user_id=self.request.user.user_id)


class UploadAvatarView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['avatar']
        user_id=request.user.user_id

        #起一个合理的名字
        file.name=f"{user_id}.png"
        storage=MinioMediaStorage()

        #如果重复就删除
        if storage.exists(f"{user_id}.png"):
            storage.delete(file.name)

        #重新创建
        storage.save(file.name,file)

        #将url存到数据库
        user=User.objects.get(user_id=user_id)
        user.avatar=storage.url(file.name)
        url=storage.url(file.name)
        user.save()

        #返回url
        return Response({'avatar': url})


class login(APIView):
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([email, password]):
            return Response({
                "fail_code":"MISSING_PARAM",
                "fail_msg":"邮箱和密码不能为空"
            },status=status.HTTP_400_BAD_REQUEST)

        # user = authenticate(email=email, password=password)
        user = User.objects.filter(email=email,password=password)
        # 反序列化user
        user = user.first()
        print(user)
        if user:
            salt = settings.SECRET_KEY
            headers = {
                'typ':'jwt',
                'alg':'HS256'
            }
            print(user.username)
            payload = {
                'user_id': user.user_id,
                'username': user.username,
                'exp':datetime.now(timezone.utc) + timedelta(minutes = 60)  # 延长token有效期为60分钟
            }

            token = jwt.encode(payload = payload, key = salt, algorithm="HS256", headers=headers)

            return Response({
                "success":True,
                "access_token":token
            })

        try:
            User.objects.get(email=email)
            return Response({
                "success": False,
                "fail_code": "WRONG_PASSWORD",
                "fail_msg": "账密错误"
            }, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "fail_code": "USER_NOT_FOUND",
                "fail_msg": "用户不存在"
            }, status=status.HTTP_404_NOT_FOUND)