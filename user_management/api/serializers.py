from rest_framework import serializers
from user_management.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id","email", "first_name", "last_name", "image")
        model = MyUser