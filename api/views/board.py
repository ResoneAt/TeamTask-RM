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
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
