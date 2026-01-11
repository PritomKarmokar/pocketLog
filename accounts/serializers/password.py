from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from applibs.logger import get_logger

logger = get_logger(__name__)

class AddPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_password(value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({
                "password": "Both Passwords does not match."
            })

        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    confirm_new_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if password == new_password:
            raise serializers.ValidationError({
                "password": "New Password cannot be same as old password."
            })

        if new_password != confirm_new_password:
            raise serializers.ValidationError({
                "password": "new_password and confirm_new_password does not match."
            })
        return attrs
    

class RequestForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()