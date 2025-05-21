import urllib3
from django.core.files.storage import default_storage
from django.shortcuts import render
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

