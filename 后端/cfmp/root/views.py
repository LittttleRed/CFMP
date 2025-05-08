from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['PUT'])
def admin_user_get(request):
    return Response({'code': "200", 'message':'admin_user_get'})
# Create your views here.
