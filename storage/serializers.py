import re
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            'id', 'user', 'file', 'original_name', 'comment',
            'size', 'upload_date', 'last_download', 'special_link'
        )
        read_only_fields = (
            'id', 'user', 'size', 'upload_date', 'last_download', 'special_link'
        )
        extra_kwargs = {
            'original_name': {'required': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну строчную букву.')
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну цифру.')
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return value

    def create(self, validated_data):
        email = validated_data.get('email', '') or None
        return User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'date_joined')
        read_only_fields = ('id', 'date_joined')