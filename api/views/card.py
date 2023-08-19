from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tasks.models import ListModel,BoardModel, CardModel,LabelModel,SubTaskModel
from api.serializers.card import ListSerializer,LabelSerializer,SubCardSerializer
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

    def create(self, request, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        srz_data = SubCardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.card = card_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        subcard = SubTaskModel.objects.get(pk=pk)
        srz_data =SubCardSerializer(instance=subcard, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        subcard = SubTaskModel.objects.get(pk=pk)
        subcard.delete()
        return Response({'message': 'subcard deleted'}, status=status.HTTP_200_OK)


class ListViewSet(ViewSet):
    queryset = ListModel.objects.all()
    
    def create(self, request, id): 
        board_instance = get_object_or_404(BoardModel, id=id)
        srz_data = ListSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.board = board_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        list = get_object_or_404(self.queryset,pk=pk)
        srz_data =ListSerializer(instance=list, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        list = get_object_or_404(self.queryset,pk=pk)
        list.delete()
        return Response({'message': 'list deleted'}, status=status.HTTP_200_OK)


class LabelViewSet(ViewSet):

    def create(self, request, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        srz_data = LabelSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.card = card_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        label = LabelModel.objects.get(pk=pk)
        srz_data =LabelSerializer(instance=label, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        label = LabelModel.objects.get(pk=pk)
        label.delete()
        return Response({'message': 'label deleted'}, status=status.HTTP_200_OK)
