from rest_framework import serializers
from tasks.models import WorkSpaceModel


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpaceModel
        fields = ['title', 'background', 'category']
