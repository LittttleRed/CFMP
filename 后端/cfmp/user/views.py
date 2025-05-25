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
from .serializers import UserSerializer, PublicUserSerializer, FollowSerializer
from .models import User, Follow
from minio import Minio
from django.conf import settings
from product.models import Product
from product.serializers import ProductSerializer
from root.serializers import ComplaintSerializer
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
            url= None
            if user.avatar:
                url = user.avatar.url
            return Response({
                "success":True,
                "access_token":token,
                "username":user.username,
                "user_id":user.user_id,
                "avatar":url
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
        # 检查文件是否存在
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['avatar']
        user = request.user

        try:
            # 保存文件到MinIO
            user.avatar.save(file.name, file)  # 自动触发存储系统保存

            # 确保用户对象保存到数据库
            user.save()

            # 获取完整的访问URL
            avatar_url = user.avatar.url

            return Response({
                'success': True,
                'avatar': avatar_url
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # 处理存储异常
            return Response({
                'error': f'Failed to upload avatar: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserProductsViewSet(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Product.objects.filter(user_id=user_id).order_by('-created_at')

class UserComplaintViewSet(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer
    def perform_create(self, serializer):
        # 自动将当前登录用户绑定到complainer_id字段
        serializer.save(complainer_id=self.request.user)

class FollowUserDetailsViewSet(ListCreateAPIView,  RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    lookup_field = 'followee_id'

    #  创建关注
    def create(self, request, *args, **kwargs):
        follower = self.request.user
        followee = User.objects.get(user_id=self.kwargs.get("followee_id"))
        Follow.objects.create(follower=follower, followee=followee)
        return Response(status=status.HTTP_201_CREATED)
    def delete(self, request, *args, **kwargs):
        follower = self.request.user
        followee = User.objects.get(user_id=self.kwargs.get("followee_id"))
        Follow.objects.filter(follower=follower, followee=followee).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FollowUserViewSet(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    """
    我关注的
    """
    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(follower=user)

class FolloweeUserViewSet(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    """
    关注我的
    """
    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(followee=user)