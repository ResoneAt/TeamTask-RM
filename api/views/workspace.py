from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from tasks.models import WorkSpaceModel
from ..serializers.workspace import WorkspaceSerializer
from django.shortcuts import get_object_or_404


class WorkspaceViewSet(ViewSet):
    
    def list(self, request):
        user_owned_workspace = WorkSpaceModel.objects.filter(owner=request.user)
        user_member_of_workspace = WorkSpaceModel.objects.filter(members=request.user)
        all_workspaces = user_owned_workspace.union(user_member_of_workspace)
        serializer = WorkspaceSerializer(all_workspaces, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        workspace = get_object_or_404(WorkSpaceModel, pk=pk)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

    def create(self, request):
        serializer = WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        workspace = get_object_or_404(WorkSpaceModel, pk=pk)
        serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        workspace = get_object_or_404(WorkSpaceModel, pk=pk)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)