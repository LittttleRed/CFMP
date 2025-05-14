from django.urls import path,register_converter
from . import views
from rest_framework import routers

#指定命名空间
app_name = 'root'
router = routers.SimpleRouter()
router.register(r'transaction', views.TransactionView)
router.register(r'user', views.UserView)
router.register(r'complaint', views.ComplaintView)
router.register(r'review', views.ComplaintReviewView)
urlpatterns = router.urls
urlpatterns += [
    path('user/get_complaint/<int:user_id>/', views.UserView.as_view({'get':'get_complaint'}), name='get_complaint')
]

