from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from accounts.models import User
from tasks.models import (
    BoardModel,
    BMembershipModel,
    CMembershipModel,
    WSMembershipModel
)
from ..serializers.membership import WorkspaceMembershipSerializer


class AddMemberToWorkspaceAPIView(APIView):
    def post(self, request, user_id, workspace_id):
        to_user = get_object_or_404(User, pk=user_id)
        workspace = get_object_or_404(WSMembershipModel, pk=workspace_id)
        membership = WSMembershipModel.objects.create(from_user=request.user,
                                                      to_user=to_user,
                                                      workspace=workspace)
        srz_data = WorkspaceMembershipSerializer(instance=membership)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class UpdateUserMembershipFromWorkspaceAPIView(APIView):
    ...


class RemoveMemberFromWorkspaceAPIView(APIView):
    ...


class WorkspaceMembersListAPIView(APIView):
    ...




class BoardMembershipViewSet(ViewSet):
    def list(self):
        ...

    def retrieve(self):
        ...

    def create(self):
        ...

    def partial_update(self):
        ...

    def destroy(self):
        ...


class CardMembershipViewSet(ViewSet):
    def list(self):
        ...

    def retrieve(self):
        ...

    def create(self):
        ...

    def partial_update(self):
        ...

    def destroy(self):
        ...
