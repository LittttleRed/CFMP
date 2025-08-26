from django.urls import path,register_converter
from . import views
from rest_framework import routers

#指定命名空间
app_name = 'root'
router = routers.SimpleRouter()
router.register(r'user', views.UserView,  basename='user')
router.register(r'complaint', views.ComplaintView, basename='complaint')
router.register(r'review', views.ComplaintReviewView, basename='review')
router.register(r'order', views.OrderView, basename="order")
router.register(r'products', views.ProductView,  basename='products')

urlpatterns = router.urls
urlpatterns += [path(r'create', views.CreatNewRoot.as_view(), name='creat')]


