from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    phone_validator = RegexValidator(
        regex=r'^\d+$',
        message="전화번호는 숫자만 입력 가능합니다."
    )

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'user_id', 'user_email', 'user_name', 'user_nickname', 'password', 'user_phone', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        return  User.objects.create_user(**validated_data)

