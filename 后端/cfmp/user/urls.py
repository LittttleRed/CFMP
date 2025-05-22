from django.urls import path,register_converter
from . import views
from rest_framework import routers

#指定命名空间
app_name = 'user'
router = routers.SimpleRouter()

urlpatterns = router.urls
urlpatterns += [
    path('user/avatar/', views.UploadAvatarView.as_view(), name='upload_portrait'),
    path('auth/login-with-password',views.login.as_view(),name='login'),
    path('user/<int:user_id>/', views.UserIdViewSet.as_view(), name='user'),
    path('user/me/',  views.UserInfoView.as_view(), name='update_user'),
    path('user/me/products/', views.UserProductsViewSet.as_view())
]
