from django.db import models
from user.models import User


class Complaint(models.Model):
    complaint_id = models.BigAutoField(primary_key=True)
    complainer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.SmallIntegerField()
    target_id = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "complaint"


class ComplaintReview(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    complaint_id = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)



class Violation(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    target_type = models.SmallIntegerField()
    target_id = models.IntegerField()
    action = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    ban_time = models.IntegerField(default=0)  # 封禁时间
    ban_type = models.SmallIntegerField(default=0)  # 封禁类型

    class Meta:
        db_table = "violation"

class Transaction(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    order_id = models.IntegerField()
    event = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction"
# Create your models here.
