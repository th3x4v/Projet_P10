from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        del validated_data["password2"]
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("User must be at least 15 years old.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "age", "email", "first_name", "last_name"]

    def to_representation(self, instance):
        """Take into account privacy choices of the users"""
        data = super().to_representation(instance)
        if not instance.can_be_contacted:
            data["email"] = None
        if not instance.can_data_be_shared:
            data["username"] = None
            data["age"] = None
            data["first_name"] = None
            data["last_name"] = None
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "age"]
