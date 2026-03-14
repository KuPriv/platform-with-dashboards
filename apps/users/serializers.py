from django.db import IntegrityError
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password", "password2"]
        # disable default UniqueValidator - handle manually in validate_email
        # (fast path) and create (race condition guard)
        extra_kwargs = {"email": {"validators": []}}

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Данный email уже зарегистрирован")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"email": "Данный email уже зарегистрирован"}
            )
