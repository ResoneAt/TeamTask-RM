from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tasks.models import ListModel, BoardModel, CardModel, LabelModel, SubTaskModel
from api.serializers.card import ListSerializer, LabelSerializer, SubCardSerializer, CardSerializer
from accounts.models import User
from rest_framework import status



class MyCards(APIView):
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def get(self, request: Response, user_id):
        user = User.objects.get(id=user_id)
        cards = CardModel.objects.filter(cmembership__user=user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CardsView(APIView):
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def get(self, request: Response, board_id):
        query_set = CardModel.objects.filter(list__board_id=board_id)
        srz_data = CardSerializer(instance=query_set, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CardAPIView(APIView):
    lookup_field = 'pk'

    def get(self, request: Response, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        srz_data = CardSerializer(instance=card)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CardCreateAPIView(APIView):
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def post(self, request: Response, list_id):
        list_instance = get_object_or_404(ListModel, id=list_id)
        srz_data = CardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.list = list_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CardUpdateAPIView(APIView):
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def put(self, request: Response, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        srz_data = CardSerializer(instance=card, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDeleteAPIView(APIView):
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def delete(self, request: Response, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        card.delete()
        return Response({'message': 'card deleted'}, status=status.HTTP_200_OK)


class SubCardViewSet(ViewSet):
    queryset = SubTaskModel.objects.all()
    serializer_class = SubCardSerializer
    lookup_field = 'pk'

    def create(self, request: Response, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        srz_data = SubCardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.card = card_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Response, pk=None):
        subcard = get_object_or_404(self.queryset, pk=pk)
        srz_data = SubCardSerializer(instance=subcard, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Response, pk):
        subcard = get_object_or_404(self.queryset, pk=pk)
        subcard.delete()
        return Response({'message': 'subcard deleted'}, status=status.HTTP_200_OK)


class ListViewSet(ViewSet):
    queryset = ListModel.objects.all()
    serializer_class = ListSerializer
    lookup_field = 'pk'

    def create(self, request: Response, board_id):
        board_instance = get_object_or_404(BoardModel, id=board_id)
        srz_data = ListSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.board = board_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Response, pk=None):
        list = get_object_or_404(self.queryset,pk=pk)
        srz_data = ListSerializer(instance=list, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Response, pk):
        list = get_object_or_404(self.queryset, pk=pk)
        list.delete()
        return Response({'message': 'list deleted'}, status=status.HTTP_200_OK)


class LabelViewSet(ViewSet):
    queryset = LabelModel.objects.all()
    serializer_class = LabelSerializer
    lookup_field = 'pk'

    def create(self, request: Response, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        srz_data = LabelSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.card = card_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Response, pk=None):
        label = get_object_or_404(self.queryset, pk=pk)
        srz_data = LabelSerializer(instance=label, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Response, pk):
        label = get_object_or_404(self.queryset, pk=pk)
        label.delete()
        return Response({'message': 'label deleted'}, status=status.HTTP_200_OK)
