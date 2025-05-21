from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
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
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_id"
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        """区分权限，对于写操作需要验证所有者
        对于读操作不需要权限
        """
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return []
        return [IsOwnerOrReadOnly()]


# 商品评价相关视图
class ProductReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取特定商品的所有评价，按时间倒序排列"""
        product_id = self.kwargs.get("product_id")
        return ProductReview.objects.filter(product_id=product_id).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(product_id=product_id)
        serializer.save(user=self.request.user, product=product)


class ProductReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductReviewSerializer
    lookup_field = "review_id"
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductReview.objects.filter(product_id=product_id)


# 收藏相关视图
class UserCollectionListAPIView(ListAPIView):
    """获取用户收藏的商品列表"""

    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Collection.objects.filter(collecter=self.request.user).order_by(
            "-create_at"
        )


class ProductCollectionView(APIView):
    """
    商品收藏相关操作的统一视图

    GET: 检查商品是否已被当前用户收藏
    POST: 收藏商品
    DELETE: 取消收藏
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        """检查商品是否已被当前用户收藏"""
        is_collected = Collection.objects.filter(
            collection__product_id=product_id, collecter=request.user
        ).exists()

        return Response({"is_collected": is_collected})

    def post(self, request, product_id):
        """收藏商品"""
        # 检查商品是否存在
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 检查是否已收藏
        if Collection.objects.filter(
            collection__product_id=product_id, collecter=request.user
        ).exists():
            return Response(
                {"detail": "您已收藏过此商品"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 创建收藏
        collection = Collection.objects.create(
            collection=product, collecter=request.user
        )

        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        """取消收藏"""
        try:
            collection = Collection.objects.get(
                collection__product_id=product_id, collecter=request.user
            )
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response(
                {"detail": "您尚未收藏此商品"}, status=status.HTTP_404_NOT_FOUND
            )


class CategoryListCreateAPIView(ListCreateAPIView):
    """获取所有分类或创建新分类"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """针对写操作
        Returns:
            返回权限级别
        """
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    """获取、更新或删除单个分类"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "category_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class ProductByCategoryAPIView(ListAPIView):
    """获取指定分类下的所有商品"""

    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Product.objects.filter(categories__category_id=category_id).order_by(
            "-created_at"
        )
