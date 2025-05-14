from rest_framework.permissions import IsAuthenticated
from typing_extensions import override
from rest_framework import views, status
from rest_framework.response import Response

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from .models import Product, Category, ProductReview, Collection
from .serializers import (
    ProductReviewSerializer,
    CategorySerializer,
    CollectionSerializer,
    ProductSerializer,
)


# 商品相关视图
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_id"


# 商品评价相关视图
class ProductReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductReview.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(product_id=product_id)
        serializer.save(user=self.request.user, product=product)


class ProductReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductReviewSerializer
    lookup_field = "review_id"

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductReview.objects.filter(product_id=product_id)


# 收藏相关视图
class UserCollectionListAPIView(ListAPIView):
    """获取用户收藏的商品列表"""

    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(collecter=self.request.user)


class CollectionCreateAPIView(CreateAPIView):
    """收藏商品"""

    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(product_id=product_id)
        serializer.save(collection=product, collecter=self.request.user)


class CollectionDestroyAPIView(DestroyAPIView):
    """取消收藏"""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        product_id = self.kwargs.get("product_id")
        return Collection.objects.get(
            collection_id=product_id, collecter=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response(
                {"detail": "您尚未收藏此商品"}, status=status.HTTP_404_NOT_FOUND
            )


class CheckCollectionStatusAPIView(APIView):
    """检查商品是否已被当前用户收藏"""

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        is_collected = Collection.objects.filter(
            collection_id=product_id, collecter=request.user
        ).exists()

        return Response({"is_collected": is_collected})
