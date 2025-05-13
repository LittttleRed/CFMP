from django.urls import path,register_converter
from . import views

#指定命名空间
app_name = 'root'
urlpatterns = [
    path('user',views.admin_user_get,name='admin_user_get'),
    #str不带'/'的字符串
    #slug有-_与英文,数字构成
    #path支持/的字符串(一般用于文件获取)
   path('TestGenericView',views.TestGenericView.as_view(),name='testgenericview'),
    path('TestDetailView/<int:log_id>/',views.TestDetailView.as_view(),name='testdetailview'),
    path('testview',views.TestView.as_view(),name='testview'),
]