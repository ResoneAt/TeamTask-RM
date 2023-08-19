from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tasks.models import ListModel,BoardModel
from api.serializers.card import ListSerializer
from rest_framework import status

class MyCardViewSet(ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...

    def partial_update(self, request, pk=None):
        ...


class CardViewSet(ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...


class SubCardViewSet(ViewSet):

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...


class ListViewSet(ViewSet):
    
    def create(self, request, board_id): 
        board_instance = get_object_or_404(BoardModel, id=board_id)
        srz_data = ListSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.board = board_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        list = ListModel.objects.get(pk=pk)
        srz_data =ListSerializer(instance=list, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        list = ListModel.objects.get(pk=pk)
        list.delete()
        return Response({'message': 'list deleted'}, status=status.HTTP_200_OK)


class LabelViewSet(ViewSet):

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...
