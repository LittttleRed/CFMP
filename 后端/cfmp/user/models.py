from django.core.validators import FileExtensionValidator
from django.db import models
from django_minio_backend import MinioBackend
from minio_storage import MinioMediaStorage


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    privilege = models.IntegerField(default=0)
    captcha = models.CharField(max_length=4,null=True,blank=True)

    class Meta:
        db_table = "user"

class ChatLog(models.Model):
    chat_id = models.BigAutoField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    content = models.TextField()
    send_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = "chat_log"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followee")

    class Meta:
        db_table = "follow"
# Create your models here.
