from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # 商品相关路由
    path(
        "product/", views.ProductListCreateAPIView.as_view(), name="product-list-create"
    ),
    path(
        "product/<int:product_id>/",
        views.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    # 商品评价相关路由
    path(
        "product/<int:product_id>/reviews/",
        views.ProductReviewListCreateAPIView.as_view(),
        name="product-review-list-create",
    ),
    path(
        "product/<int:product_id>/reviews/<int:review_id>/",
        views.ProductReviewDetailAPIView.as_view(),
        name="product-review-detail",
    ),
    # 收藏相关路由
    path(
        "product/collections/",
        views.UserCollectionListAPIView.as_view(),
        name="user-collections",
    ),
    path(
        "product/<int:product_id>/collection/",
        views.CollectionCreateAPIView.as_view(),
        name="collect-product",
    ),
    path(
        "product/<int:product_id>/collection/cancel/",
        views.CollectionDestroyAPIView.as_view(),
        name="cancel-collection",
    ),
    path(
        "product/<int:product_id>/collection/status/",
        views.CheckCollectionStatusAPIView.as_view(),
        name="check-collection-status",
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
