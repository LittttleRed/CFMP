from django.db import models
from user.models import User


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,db_column="user")
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    product_img = models.JSONField()
    categories = models.ManyToManyField("Category", related_name="products")

    class Meta:
        db_table = "product"


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"


class ProductReview(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 星
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_review"
        unique_together = ("product", "user")  # 每个用户对同一商品只能评价一次


class Collection(models.Model):
    collection = models.ForeignKey(Product, on_delete=models.CASCADE)
    collecter = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collection"
        unique_together = ("collection", "collecter")


# Create your models here.
