from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used for registering new users and includes fields for
    username, password, password confirmation, age, contact preferences, email,
    first name, and last name.
    """

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
            "email",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        """
        Custom validation method to check if the provided passwords match.

        Args:
            attrs (dict): Dictionary containing the serializer's validated data.

        Returns:
            dict: The validated data if passwords match.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        """
        Custom method to create a new user instance.

        Args:
            validated_data (dict): Validated data from the serializer.

        Returns:
            User: The newly created User instance.
        """
        del validated_data["password2"]
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user

    def validate_age(self, value):
        """
        Custom validation method to check if the user's age is at least 15 years old.

        Args:
            value (int): The user's age.

        Returns:
            int: The validated age value.

        Raises:
            serializers.ValidationError: If the age is less than 15.
        """
        if value < 15:
            raise serializers.ValidationError("User must be at least 15 years old.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.

    This serializer is used to represent user details, including fields like
    username, age, email, first name, and last name, while respecting user
    privacy choices.
    """

    class Meta:
        model = User
        fields = ["id", "username", "age", "email", "first_name", "last_name"]

    def to_representation(self, instance):
        """
        Customize the representation of user data, considering privacy preferences.

        Args:
            instance (User): The User instance to represent.

        Returns:
            dict: The serialized representation of user data.
        """
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
