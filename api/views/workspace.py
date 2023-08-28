from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from tasks.models import WorkSpaceModel
from ..serializers.workspace import WorkspaceSerializer
from django.shortcuts import get_object_or_404


class WorkspaceViewSet(ViewSet):
    serializer_class = WorkspaceSerializer
    
    def list(self, request):
        if request.user.is_authenticated:
            user_owned_workspace = WorkSpaceModel.objects.filter(owner=request.user)
            user_member_of_workspace = WorkSpaceModel.objects.filter(members=request.user)
            all_workspaces = user_owned_workspace.union(user_member_of_workspace)
            serializer = WorkspaceSerializer(all_workspaces, many=True)
            return Response(serializer.data)
        else:
            return Response('you have to login first')
        
    def retrieve(self, request, pk=None):
        workspace = get_object_or_404(WorkSpaceModel, pk=pk)
        if request.user.is_authenticated:
            serializer = WorkspaceSerializer(workspace)
            return Response(serializer.data)
        else:
            return Response('you have to login first')

    def create(self, request):
        if request.user.is_authenticated:
            serializer = WorkspaceSerializer(data=request.data)
            if serializer.is_valid():
                workspace = serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('you have to login first')
         
    def partial_update(self, request, pk=None):
        workspace = get_object_or_404(WorkSpaceModel, pk=pk, owner=request.user)
        if workspace.owner == request.user:
            serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response('permission denied, you are not the workspace owner')

    def destroy(self, request, pk=None):
        if workspace.owner == request.user:
            workspace = get_object_or_404(WorkSpaceModel, pk=pk, owner=request.user)
            workspace.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('permission denied, you are not the workspace owner')
