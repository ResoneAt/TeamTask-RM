from rest_framework import serializers

from api.serializers.accounts import UserSerializer
from tasks.models import WSMembershipModel, BMembershipModel


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    to_user = UserSerializer()
    class Meta:
        model = WSMembershipModel
        fields = '__all__'
        extra_fields = {
            'from_user': {'read_only': True},
            'to_user': {'read_only': True},
            'workspace': {'read_only': True}
        }


class BoardMembershipSerializer(serializers.ModelSerializer):
    to_user = UserSerializer()

    class Meta:
        model = BMembershipModel
        fields = '__all__'
        extra_fields = {
            'from_user': {'read_only': True},
            'to_user': {'read_only': True},
            'board': {'read_only': True}
        }


class CardMembershipSerializer(serializers.ModelSerializer):
    ...

