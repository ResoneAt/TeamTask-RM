from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tasks.models import ListModel,BoardModel, CardModel,LabelModel,SubTaskModel
from api.serializers.card import ListSerializer,LabelSerializer,SubCardSerializer,\
                                 CardSerializer
from accounts.models import User
from rest_framework import status

class MyCards(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        cards = CardModel.objects.filter(cmembership__user=user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CardsView(APIView):    
    def get(self, request,board_id):
        query_set = CardModel.objects.filter(list__board_id=board_id)
        srz_data = CardSerializer(instance=query_set, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
      
class CardView(APIView):
    def get(self, request, card_id):
        card = get_object_or_404(CardModel, id=card_id)


class CardCreate(APIView):
    def post(self, request, list_id):
        list_instance = get_object_or_404(ListModel, id=list_id)
        srz_data = CardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.list = list_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class CardUpdate(APIView):
    def put(self, request, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        srz_data = CardSerializer(instance=card,data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class CardDelete(APIView):
    def delete(self, request, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        card.delete()
        return Response({'message': 'card deleted'}, status=status.HTTP_200_OK)


class SubCardViewSet(ViewSet):
    queryset = SubTaskModel.objects.all()

    def create(self, request, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        srz_data = SubCardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.card = card_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        subcard = get_object_or_404(self.queryset, pk=pk)
        srz_data =SubCardSerializer(instance=subcard, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        subcard = get_object_or_404(self.queryset, pk=pk)
        subcard.delete()
        return Response({'message': 'subcard deleted'}, status=status.HTTP_200_OK)


class ListViewSet(ViewSet):
    queryset = ListModel.objects.all()
    
    def create(self, request, board_id): 
        board_instance = get_object_or_404(BoardModel, id=board_id)
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
    queryset = LabelModel.objects.all()

    def create(self, request, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        srz_data = LabelSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.card = card_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        label = get_object_or_404(self.queryset, pk=pk)
        srz_data =LabelSerializer(instance=label, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        label = get_object_or_404(self.queryset, pk=pk)
        label.delete()
        return Response({'message': 'label deleted'}, status=status.HTTP_200_OK)
