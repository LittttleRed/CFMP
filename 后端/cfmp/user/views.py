import urllib3
import jwt
import datetime
from datetime import datetime, timedelta, timezone
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate
from minio_storage import MinioMediaStorage
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import UserSerializer, PublicUserSerializer, FollowSerializer, ChatLogSerializer, MessagesSerializer
from .models import User, Follow, ChatLog, Messages
from .serializers import UserSerializer, PublicUserSerializer
from .models import User
from .models import Captcha
from minio import Minio
from django.conf import settings
from jwt import exceptions
# Create your views here.
import re

from .pagination import StandardResultsSetPagination


def send_sms_code(to_email):
    # 生成邮箱验证码
    sms_code = '%06d' % random.randint(0, 999999)
    EMAIL_FROM = "3417934680@qq.com"  # 邮箱来自
    email_title = '邮箱激活'
    email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    if send_status != 0:
        # 存储验证码
        captcha = Captcha.objects.create(
            captcha=sms_code,
            email=to_email
        )
        captcha.save()
    return send_status

def varify_captcha(email,captcha):
    captchaObj = Captcha.objects.filter(email=email).last()
    if  not captchaObj:  # 验证码不存在
        return Response({
            "fail_code":"CAPTCHA_NOT_FOUND",
            "fail_msg":"验证码不存在"
        },status=status.HTTP_400_BAD_REQUEST)
    if captcha != captchaObj.captcha:
        return Response({
            "fail_code":"CAPTCHA_ERROR",
            "fail_msg":"验证码错误"
        },status=status.HTTP_400_BAD_REQUEST)
    if captchaObj.created_at < datetime.now(timezone.utc) - timedelta(minutes=2):  # 验证码有效时间2分钟
        return Response({
            "fail_code":"CAPTCHA_EXPIRED",
            "fail_msg":"验证码已过期"
        },status=status.HTTP_400_BAD_REQUEST)
    if captchaObj.is_used:  # 验证码已使用
        return Response({
            "fail_code":"CAPTCHA_ERROR",
            "fail_msg":"验证码错误"
        },status=status.HTTP_400_BAD_REQUEST)
    captchaObj.is_used = True
    captchaObj.save()
    return 0

class CaptchaView(APIView):
    def post(self, request):
        email = request.data.get('email')
        scene = request.data.get('scene')
        if not all([email, scene]):
            return Response({
                "fail_code":"MISSING_PARAM",
                "fail_msg":"缺少参数"
            },status=status.HTTP_400_BAD_REQUEST)
        common_scene = {'register','login','forget'}
        need_token_scene = {'change_email','change_password'}
        user = User.objects.filter(email=email)
        if user.exists():
            return Response({
                "fail_code": "USER_EXIST",
                "fail_msg": "用户已存在"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return Response({
                "fail_code": "EMAIL_FORMAT_ERROR",
                "fail_msg": "邮箱格式错误"
            }, status=status.HTTP_400_BAD_REQUEST)
        if scene in common_scene:
            if send_sms_code(email) != 0:
                return Response({
                    "success":True,
                    "msg":"发送成功"
                })
            else:
                return Response({
                    "success":False,
                    "msg":"发送失败"
                })
        elif scene in need_token_scene:
            auth = request.META.get('HTTP_AUTHORIZATION', '')
            if  not auth:
                return Response({
                    "success":False,
                    "msg":"验证失败"
                })
            JWTAuthentication.authenticate(self,request)
            if send_sms_code(email) != 0:
                return Response({
                    "success":True,
                    "msg":"发送成功"
                })
            else:
                return Response({
                    "success":False,
                    "msg":"发送失败"
                })
        else:
            return Response({
                "success":False,
                "msg":"参数错误"
            })
class RegisterView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password_repeat = request.data.get('password_repeat')
        email = request.data.get('email')
        captcha = request.data.get('captcha')
        #print(username,password,password_repeat,email,captcha)
        if not all([username, password, password_repeat, email, captcha]):
            return Response({
                "fail_code":"MISSING_PARAM",
                "fail_msg":"缺少参数"
            },status=status.HTTP_400_BAD_REQUEST)

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
        #反序列化user
        user = user.first()
        
        print(user)
        if user:
            salt = settings.SECRET_KEY

            headers ={
                'typ':'jwt',
                'alg':'HS256'
            }
            print(user.username)
            payload = {
                'user_id': user.user_id,
                'username': user.username,
                'exp':datetime.now(timezone.utc) + timedelta(minutes = 1)
            }

            token = jwt.encode(payload = payload, key = salt,algorithm="HS256", headers=headers)

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
