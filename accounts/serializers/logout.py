from rest_framework import serializers

class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()