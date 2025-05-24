import uuid

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnly, IsAdmin
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from .models import (
    Product,
    Category,
    ProductReview,
    Collection,
    ProductMedia,
)
from .serializers import (
    ProductReviewSerializer,
    CategorySerializer,
    CollectionSerializer,
    ProductSerializer,
    ProductMediaSerializer,
)
from .filters import ProductFilter


# 商品相关视图
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        # 保存商品基本信息
        product = serializer.save(user=self.request.user)
        print(self.request.FILES.getlist("media"))
        # 处理分类
        if "categories" in self.request.data:
            category_ids = (
                self.request.data.getlist("categories")
                if hasattr(self.request.data, "getlist")
                else self.request.data.get("categories", [])
            )
            if not isinstance(category_ids, list):
                category_ids = [category_ids]

            for category_id in category_ids:
                try:
                    category = Category.objects.get(category_id=category_id)
                    product.categories.add(category)
                except Category.DoesNotExist:
                    pass  # 忽略不存在的分类

        # 处理上传的图片
        if "media" in self.request.FILES:
            media_files = self.request.FILES.getlist("media")

            # 第一张图片设为主图
            is_first = True

            for media_file in media_files:
                # 创建媒体文件记录
                media_file.name = f"{product.product_id}+'_'+{uuid.uuid4().hex}.jpg"
                ProductMedia.objects.create(
                    product=product,
                    media=media_file,
                    is_main=is_first,  # 第一张图片设为主图
                )

                # 更新标志
                if is_first:
                    is_first = False


# 商品图片相关视图
class ProductMediaListView(APIView):
    """
    商品图片列表相关操作

    GET: 获取商品的所有图片
    POST: 为商品添加图片
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        """获取商品的所有图片"""
        try:
            product = Product.objects.get(product_id=product_id)
            media = ProductMedia.objects.filter(product=product)
            serializer = ProductMediaSerializer(media, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, product_id):
        """为商品添加图片"""
        try:
            # 检查商品是否存在
            product = Product.objects.get(product_id=product_id)

            # 检查用户是否有权限
            if request.user != product.user:
                return Response(
                    {"detail": "您没有权限修改此商品"}, status=status.HTTP_403_FORBIDDEN
                )

            # 处理上传的图片
            if "media" in request.FILES:
                media_files = request.FILES.getlist("media")

                # 检查是否已有主图
                has_main_image = ProductMedia.objects.filter(
                    product=product, is_main=True
                ).exists()
                set_as_main = not has_main_image  # 如果没有主图，则将第一张设为主图

                created_media = []
                for media_file in media_files:
                    media = ProductMedia.objects.create(
                        product=product, media=media_file, is_main=set_as_main
                    )
                    created_media.append(media)

                    # 更新标志
                    if set_as_main:
                        set_as_main = False

                serializer = ProductMediaSerializer(created_media, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"detail": "未提供图片"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)


class ProductMediaDetailView(APIView):
    """
    单个商品图片操作

    GET: 获取单个图片详情
    PUT: 更新图片（如设置为主图）
    DELETE: 删除图片
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, media_id):
        """获取单个图片详情"""
        try:
            product = Product.objects.get(product_id=product_id)
            media = ProductMedia.objects.get(media_id=media_id, product=product)
            serializer = ProductMediaSerializer(media)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
        except ProductMedia.DoesNotExist:
            return Response({"detail": "图片不存在"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id, media_id):
        """更新图片信息（如设置为主图）"""
        try:
            # 检查商品是否存在
            product = Product.objects.get(product_id=product_id)

            # 检查用户是否有权限
            if request.user != product.user:
                return Response(
                    {"detail": "您没有权限修改此商品"}, status=status.HTTP_403_FORBIDDEN
                )

            # 获取图片
            media = ProductMedia.objects.get(media_id=media_id, product=product)

            # 处理请求数据
            if "is_main" in request.data and request.data["is_main"]:
                media.is_main = True
                media.save()  # 自动处理其他图片的is_main状态

            serializer = ProductMediaSerializer(media)
            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
        except ProductMedia.DoesNotExist:
            return Response({"detail": "图片不存在"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id, media_id):
        """删除商品图片"""
        try:
            # 检查商品是否存在
            product = Product.objects.get(product_id=product_id)

            # 检查用户是否有权限
            if request.user != product.user:
                return Response(
                    {"detail": "您没有权限修改此商品"}, status=status.HTTP_403_FORBIDDEN
                )

            # 删除图片
            try:
                media = ProductMedia.objects.get(media_id=media_id, product=product)
                is_main = media.is_main
                media.delete()

                # 如果删除的是主图，设置新的主图
                if is_main:
                    new_main = ProductMedia.objects.filter(product=product).first()
                    if new_main:
                        new_main.is_main = True
                        new_main.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            except ProductMedia.DoesNotExist:
                return Response(
                    {"detail": "图片不存在"}, status=status.HTTP_404_NOT_FOUND
                )

        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_id"
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        """
        区分权限，对于写操作需要验证所有者
        对于读操作不需要权限
        """
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return []
        return [IsOwnerOrReadOnly()]

    def perform_update(self, serializer):
        # 保存商品基本信息
        product = serializer.save()

        # 处理分类
        if "categories" in self.request.data:
            category_ids = (
                self.request.data.getlist("categories")
                if hasattr(self.request.data, "getlist")
                else self.request.data.get("categories", [])
            )
            if not isinstance(category_ids, list):
                category_ids = [category_ids]

            # 清除现有分类
            product.categories.clear()

            # 添加新分类
            for category_id in category_ids:
                try:
                    category = Category.objects.get(category_id=category_id)
                    product.categories.add(category)
                except Category.DoesNotExist:
                    pass  # 忽略不存在的分类


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
        
        # 检查用户是否已经评论过该商品
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"detail": "您已经评论过该商品"})
            
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
        return [IsAdmin()]


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    """获取、更新或删除单个分类"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "category_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdmin()]


class ProductByCategoryAPIView(ListAPIView):
    """获取指定分类下的所有商品"""

    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Product.objects.filter(categories__category_id=category_id).order_by(
            "-created_at"
        )
