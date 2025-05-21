from rest_framework import serializers
from .models import (
    Product,
    Category,
    ProductReview,
    Collection,
    ProductMedia,
    ProductReviewMedia,
)
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ["media_id", "media"]


class ProductReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviewMedia
        fields = ["review_media_id", "media"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    # 反向引用外键，需要使用related_name
    media = ProductMediaSerializer(source="media", many=True, read_only=True)

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
            "categories",
            "media",
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # 反向引用外键，需要使用related_name
    media = ProductReviewMediaSerializer(source="media", many=True, read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "review_id",
            "product",
            "user",
            "rating",
            "comment",
            "created_at",
            "media",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    collecter = UserSerializer(read_only=True)
    collection = ProductSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ["collection", "collecter", "create_at"]
