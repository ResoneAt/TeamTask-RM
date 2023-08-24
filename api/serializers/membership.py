from rest_framework import serializers

from api.serializers.accounts import UserSerializer
from tasks.models import WSMembershipModel


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    to_user = UserSerializer()
    class Meta:
        model = WSMembershipModel
        fields = '__all__'
        # extra_fields = {
        #     'from_user': {'read_only': True},
        #     'to_user': {'read_only': True},
        #     'workspace': {'read_only': True}
        # }


class BoardMembershipSerializer(serializers.ModelSerializer):
    ...


class CardMembershipSerializer(serializers.ModelSerializer):
    ...

