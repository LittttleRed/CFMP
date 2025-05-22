import urllib3
import jwt
import datetime
from datetime import datetime, timedelta, timezone
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.contrib.auth import authenticate
from minio_storage import MinioMediaStorage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import UserSerializer
from .models import User
from minio import Minio
from django.conf import settings
from jwt import exceptions
# Create your views here.



class UploadPortraitView(APIView):
    def post(self, request):
        file=request.FILES['image']
        file.name='test1.jpg'
        storage=MinioMediaStorage()
        storage.save(file.name,file)
        return Response(status=status.HTTP_200_OK)

    def get(self,request):
        storage=MinioMediaStorage()
        date={'image':storage.url('test.jpg')}
        return Response(date,status=status.HTTP_200_OK)

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