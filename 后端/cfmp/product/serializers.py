from rest_framework import serializers
from .models import (
    Product,
    Category,
    ProductReview,
    Collection,
    ProductMedia,
)
from user.serializers import PublicUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ["media_id", "media", "is_main", "created_at"]



class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    #使用不敏感的序列化方式
    user = PublicUserSerializer(read_only=True)
    # 反向引用外键，需要使用related_name
    media = ProductMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "product_id",
            "user",
            "title",
            "description",
            "price",
            "status",
            "created_at",
            "product_img",
            "categories",
            "media",
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "review_id",
            "product",
            "user",
            "rating",
            "comment",
            "created_at",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    collecter = PublicUserSerializer(read_only=True)
    collection = ProductSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ["collection", "collecter", "create_at"]
