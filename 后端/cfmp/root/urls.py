from django.urls import path,register_converter
from . import views
from rest_framework import routers

#指定命名空间
app_name = 'root'
router = routers.SimpleRouter()
router.register(r'transaction', views.TransactionView)
router.register(r'user', views.UserView)
urlpatterns = router.urls

