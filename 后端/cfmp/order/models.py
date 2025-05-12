from django.db import models
from user.models import User
from product.models import Product

class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.SmallIntegerField(default=2)

    class Meta:
        db_table = "order"
# Create your models here.
