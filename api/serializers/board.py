from rest_framework import serializers

from api.serializers.workspace import WorkspaceSerializer
from tasks.models import BoardModel


class BoardSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer()
    class Meta:
        model = BoardModel
        fields = "__all__"
