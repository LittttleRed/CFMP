from django.urls import path,register_converter
from . import views
from rest_framework import routers

#指定命名空间
app_name = 'user'
router = routers.SimpleRouter()

urlpatterns = router.urls
urlpatterns += [
    path('test_img/', views.UploadPortraitView.as_view(), name='upload_portrait'),
]
