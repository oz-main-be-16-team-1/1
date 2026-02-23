from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    user_pw = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'user_email', 'user_name', 'user_nickname', 'user_pw', 'user_phone', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        return  User.objects.create(**validated_data)

