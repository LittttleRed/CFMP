from rest_framework import serializers
from .models import Product, Category, ProductReview, Collection


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

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
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Collection
        fields = ["collection", "collecter", "create_at"]
