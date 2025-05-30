from django.urls import path,register_converter
from . import views
from rest_framework import routers

#指定命名空间
app_name = 'root'
router = routers.SimpleRouter()
router.register(r'user', views.UserView)
router.register(r'complaint', views.ComplaintView)
router.register(r'review', views.ComplaintReviewView)
router.register(r'order', views.OrderView)
router.register(r'products', views.ProductView)
urlpatterns = router.urls
urlpatterns += []


