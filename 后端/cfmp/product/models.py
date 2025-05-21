from django.db import models
from user.models import User
from django_minio_backend import MinioBackend


class Product(models.Model):
    """Product

    Attributes:
        product_id: primary_key(not nessary)
        user: model
        title: CharField
        description: TextField
        price: DecimalField
        status:  default=0
        created_at: DateTimeField(not nessary)
        categories: model(related_name="products")
    """

    product_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("Category", related_name="products")

    class Meta:
        db_table = "product"


class ProductMedia(models.Model):
    """ProductMedia

    Attributes:
        media_id: primary_key(not nessary)
        product: model(related_name="media")
        media: FileField
    """

    media_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="media")
    media = models.FileField(
        upload_to="product_media/",
        storage=MinioBackend(),
        null=True,
        blank=True,
    )

    class Meta:
        da_table = "product_media"


class Category(models.Model):
    """Category

    Attributes:
        category_id: primary_key(not nessary)
        name: CharField
    """

    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"


class ProductReview(models.Model):
    """ProductReview

    Attributes:
        review_id: primary_key(not nessary)
        product: model(related_name="reviews")
        user: model
        rating: 1-5
        comment: TextField
        created_at: DateTimeField(not nessary)
    """

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


class ProductReviewMedia(models.Model):
    """ProductReviewMedia

    Attributes:
        review_media_id: primary_key(not nessary)
        review: model(related_name="media")
        media: FileField
    """

    review_media_id = models.BigAutoField(primary_key=True)
    review = models.ForeignKey(
        ProductReview, on_delete=models.CASCADE, related_name="media"
    )
    media = models.FileField(
        upload_to="review_media/",
        storage=MinioBackend(),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "product_review_media"


class Collection(models.Model):
    """Collection

    Attributes:
        collection: model(related_name="collections")
        collecter: model
        create_at: DateTimeField(not nessary)
    """

    collection = models.ForeignKey(Product, on_delete=models.CASCADE)
    collecter = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collection"
        unique_together = ("collection", "collecter")
