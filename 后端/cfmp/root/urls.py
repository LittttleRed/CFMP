from django.urls import path,register_converter
from . import views

#指定命名空间
app_name = 'root'
urlpatterns = [
    path('user/',views.admin_user_get,name='admin_user_get'),
]