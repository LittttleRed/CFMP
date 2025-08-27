from rest_framework import serializers
from product import ProductSerializer
from . import models
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaint
        fields = '__all__'

class ComplaintReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplaintReview
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
