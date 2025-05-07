from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    privilege = models.IntegerField(default=0)

    class Meta:
        db_table = "user"


#  商品
#  图片存储暂时采用 JSONField 格式存储, 后期商品负责人可以根据需求更改
class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.SmallIntegerField(default=2)

    class Meta:
        db_table = "order"


class ChatLog(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    content = models.TextField()
    send_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = "chat_log"


class TransactionLog(models.Model):
    log_id = models.IntegerField(primary_key=True)
    order_id = models.IntegerField()
    event = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction_log"


class Follow(models.Model):
    follower_id = models.IntegerField()
    followee_id = models.IntegerField()

    class Meta:
        db_table = "follow"


class Collection(models.Model):
    collection_id = models.IntegerField()
    collecter_id = models.IntegerField()

    class Meta:
        db_table = "collection"
        unique_together = (("collection_id", "collecter_id"),)


class Complaint(models.Model):
    complaint_id = models.IntegerField(primary_key=True)
    complainer_id = models.IntegerField()
    target_type = models.SmallIntegerField()
    target_id = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=0)
    reviewer_id = models.IntegerField(default=-1)
    reviewed_at = models.DateTimeField(default=None)
    result = models.CharField(max_length=100)

    class Meta:
        db_table = "complaint"


class ViolationRecord(models.Model):
    record_id = models.IntegerField(primary_key=True)
    target_type = models.SmallIntegerField()
    target_id = models.IntegerField()
    action = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    ban_time = models.IntegerField(default=0)  # 封禁时间
    ban_type = models.SmallIntegerField(default=0)  # 封禁类型
    class Meta:
        db_table = "violation_record"
