from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from tasks.models import BoardModel
from ..serializers.board import BoardSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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


class BoardView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        all_board = BoardModel.objects.all()
        ser_data = BoardSerializer(instance=all_board, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = BoardSerializer(data=request.POST)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        board = BoardModel.objects.get(pk=pk)
        ser_data = BoardSerializer(instance=board, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        board = BoardModel.objects.get(pk=pk)
        board.delete()
        return Response({"message": 'you successfully delete board'})
