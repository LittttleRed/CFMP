
from minio_storage import MinioMediaStorage
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.



class UploadPortraitView(APIView):
    def post(self, request):
        file=request.FILES['image']
        file.name='test.jpg'
        storage=MinioMediaStorage()
        storage.save(file.name,file)
        return Response(status=status.HTTP_200_OK)
