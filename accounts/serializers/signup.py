from rest_framework import serializers

from accounts.models import User

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError(detail="An User with this email address already exists.", code="UAE400")
        return attrs
