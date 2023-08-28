from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.models import BoardModel, WorkSpaceModel
from ..serializers.board import BoardSerializer
from permissions import IsWorkSpaceOwner, IsBoardOwner, IsWorkSpaceMember

# class BoardViewSet(ViewSet):
#     def list(self, request):
#         # workspace
#         ...
#
#     def retrieve(self, request, pk=None):
#         # get board
#         ...
#
#     def create(self, request):
#         # create board
#         ...
#
#     def partial_update(self, request, pk=None):
#         ...
#
#     def destroy(self, request):
#         # delete board
#         ...


class BoardListView(APIView):
    permission_classes = [IsWorkSpaceMember]

    def get(self, request, workspace_id):
        workspace = WorkSpaceModel.objects.get(pk=workspace_id)
        self.check_object_permissions(self, workspace)
        all_board = BoardModel.objects.filter(workspace=workspace)
        ser_data = BoardSerializer(instance=all_board, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BoardCreateView(APIView):
    permission_classes = [IsWorkSpaceOwner | IsWorkSpaceMember]

    def post(self, request, workspace_id):
        data = BoardSerializer(data=request.POST)
        workspace = WorkSpaceModel.objects.get(pk=workspace_id)
        self.check_object_permissions(self, workspace)
        if data.is_valid():
            data.save(commit=False)
            data.workspce = workspace
            data.save()
            return Response(data.data, status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardUpdateView(APIView):
    permission_classes = [IsWorkSpaceOwner | IsWorkSpaceMember | IsBoardOwner]

    def put(self, request, pk):
        board = BoardModel.objects.get(pk=pk)
        self.check_object_permissions(self, board.workspace)
        self.check_object_permissions(self, board)
        ser_data = BoardSerializer(instance=board, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDeleteView(APIView):
    permission_classes = [IsWorkSpaceOwner | IsWorkSpaceMember | IsBoardOwner]

    def delete(self, request, pk):
        board = BoardModel.objects.get(pk=pk)
        self.check_object_permissions(self, board.workspace)
        self.check_object_permissions(self, board)
        board.delete()
        return Response({"message": 'you successfully delete board'}, status=status.HTTP_200_OK)
