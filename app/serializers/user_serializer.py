from rest_framework import serializers
from models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'created_at']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user