from rest_framework import serializers
from . import models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id', 'username', 'avatar']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follow
        fields = '__all__'