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
    WSMembershipModel,
    WorkSpaceModel
)
from ..serializers.membership import WorkspaceMembershipSerializer, BoardMembershipSerializer


class AddMemberToWorkspaceAPIView(APIView):
    def post(self, request, user_id, workspace_id):
        to_user = get_object_or_404(User, pk=user_id)
        workspace = get_object_or_404(WorkSpaceModel, pk=workspace_id)
        membership = WSMembershipModel.objects.create(from_user=request.user,
                                                      to_user=to_user,
                                                      workspace=workspace)
        srz_data = WorkspaceMembershipSerializer(instance=membership)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class UpdateMembershipFromWorkspaceAPIView(APIView):
    def patch(self, request, membership_id):
        membership = get_object_or_404(WSMembershipModel,
                                       pk=membership_id)
        srz_data = WorkspaceMembershipSerializer(instance=membership,
                                                 data=request.POST,
                                                 partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveMemberFromWorkspaceAPIView(APIView):
    def delete(self, request, membership_id):
        membership = get_object_or_404(WSMembershipModel, pk=membership_id)
        membership.delete()
        return Response({'message': 'user removed'}, status=status.HTTP_200_OK)


class WorkspaceMembersListAPIView(APIView):
    def get(self, request, workspace_id):
        workspace = get_object_or_404(WorkSpaceModel, pk=workspace_id)
        members = (WSMembershipModel.objects.select_related('to_user')
                   .filter(workspace=workspace))
        srz_data = WorkspaceMembershipSerializer(instance=members, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class AddMemberToBoardAPIView(APIView):
    def post(self, request, user_id, board_id):
        to_user = get_object_or_404(User, pk=user_id)
        board = get_object_or_404(BoardModel, pk=board_id)
        membership = BMembershipModel.objects.create(from_user=request.user,
                                                     to_user=to_user,
                                                     board=board)
        srz_data = BoardMembershipSerializer(instance=membership)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

class UpdateMembershipFromBoardAPIView(APIView):
    ...


class RemoveMemberFromBoardAPIView(APIView):
    ...


class BoardMembersListAPIView(APIView):
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
