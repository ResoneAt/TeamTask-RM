from rest_framework import serializers
from accounts.models import User


class SignUpSerializer(serializers.ModelSerializer):
    ...


class ProfileSerializer(serializers.ModelSerializer):
    ...


class NotificationSerializer(serializers.ModelSerializer):
    ...

