from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tasks.models import ListModel, BoardModel, CardModel, LabelModel, SubTaskModel
from api.serializers.card import ListSerializer, LabelSerializer, SubCardSerializer, CardSerializer
from accounts.models import User
from rest_framework import status
from permissions import IsCardMember, IsBoardMember, IsBoardOwner


class MyCardsAPIView(APIView):
    permission_classes = [IsCardMember,]
    serializer_class = CardSerializer
    lookup_field = 'pk'
    queryset = CardModel.objects.all()

    def get(self, request: Response, user_id):
        user = User.objects.get(id=user_id)
        cards = cache.get('my_cards')
        if not cards:
            cards = CardModel.objects.filter(cmembership__user=user)
            cache.set('my_cards', '')
        self.check_object_permissions(request, cards)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CardsAPIView(APIView):
    permission_classes = [IsBoardMember,]
    serializer_class = CardSerializer
    lookup_field = 'pk'
    queryset = CardModel.objects.all()

    def get(self, request: Response, board_id):
        query_set = CardModel.objects.filter(list__board_id=board_id)
        board = get_object_or_404(BoardModel, id=board_id)
        self.check_object_permissions(request, board)
        srz_data = CardSerializer(instance=query_set, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CardAPIView(APIView):
    permission_classes = [IsBoardMember,]
    serializer_class = CardSerializer

    def get(self, request: Response, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        self.check_object_permissions(request, card.list.board)
        srz_data = CardSerializer(instance=card)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CardCreateAPIView(APIView):
    permission_classes = [IsBoardOwner,]
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def post(self, request: Response, list_id):
        list_instance = get_object_or_404(ListModel, id=list_id)
        self.check_object_permissions(request, list_instance.board)
        srz_data = CardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.object.list = list_instance
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CardUpdateAPIView(APIView):
    permission_classes = [IsBoardOwner | IsCardMember]
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def put(self, request: Response, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        self.check_object_permissions(request, card)
        self.check_object_permissions(request, card.list.board)
        srz_data = CardSerializer(instance=card, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDeleteAPIView(APIView):
    permission_classes = [IsBoardOwner]
    serializer_class = CardSerializer
    lookup_field = 'pk'

    def delete(self, request: Response, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        self.check_object_permissions(request, card.list.board)
        card.delete()
        return Response({'message': 'card deleted'}, status=status.HTTP_200_OK)


class SubCardViewSet(ViewSet):
    queryset = SubTaskModel.objects.all()
    serializer_class = SubCardSerializer
    lookup_field = 'pk'

    def create(self, request: Response, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        if card_instance.cmembershipmodel_set.filter(to_user=request.user).exists():
            srz_data = SubCardSerializer(data=request.data)
            if srz_data.is_valid():
                srz_data.object.card = card_instance
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_201_CREATED)
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           Response('permission denied, you are not a member of this card')
           
    def partial_update(self, request: Response, pk=None):
        subcard = get_object_or_404(self.queryset, pk=pk)
        if subcard.card.cmembershipmodel_set.filter(to_user=request.user).exists():
            srz_data = SubCardSerializer(instance=subcard, data=request.POST, partial=True)
            if srz_data.is_valid():
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_200_OK)
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           Response('permission denied, you are not a member of this card')

    def destroy(self, request: Response, pk):
        subcard = get_object_or_404(self.queryset, pk=pk)
        if subcard.card.cmembershipmodel_set.filter(to_user=request.user).exists():
            subcard.delete()
            return Response({'message': 'subcard deleted'}, status=status.HTTP_200_OK)
        else:
           Response('permission denied, you are not a member of this card')


class ListViewSet(ViewSet):
    queryset = ListModel.objects.all()
    serializer_class = ListSerializer
    lookup_field = 'pk'

    def create(self, request: Response, board_id):
        board_instance = get_object_or_404(BoardModel, id=board_id)
        if board_instance.owner == request.user:
            srz_data = ListSerializer(data=request.data)
            if srz_data.is_valid():
                srz_data.object.board = board_instance
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_201_CREATED)
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response('permission denied, you are not board owner')

    def partial_update(self, request, pk=None):
        list = get_object_or_404(self.queryset, pk=pk)
        if list.board.owner == request.user:
            srz_data = ListSerializer(instance=list, data=request.POST, partial=True)
            if srz_data.is_valid():
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_200_OK)
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response('permission denied, you are not board owner')

    def destroy(self, request: Response, pk):
        list = get_object_or_404(self.queryset, pk=pk)
        if list.board.owner == request.user:
            list.delete()
            return Response({'message': 'list deleted'}, status=status.HTTP_200_OK)
        else:
            Response('permission denied, you are not board owner')

class LabelViewSet(ViewSet):
    queryset = LabelModel.objects.all()
    serializer_class = LabelSerializer
    lookup_field = 'pk'

    def create(self, request: Response, card_id):
        card_instance = get_object_or_404(CardModel, id=card_id)
        if card_instance.cmembershipmodel_set.filter(to_user=request.user).exists()\
            or card_instance.list.board.owner == request.user:
            srz_data = LabelSerializer(data=request.data)
            if srz_data.is_valid():
                srz_data.object.card = card_instance
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_201_CREATED)
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response('create label permission denied')

    def partial_update(self, request: Response, pk=None):
        label = get_object_or_404(self.queryset, pk=pk)
        if label.card.cmembershipmodel_set.filter(to_user=request.user).exists()\
            or label.card.list.board.owner == request.user:
            srz_data = LabelSerializer(instance=label, data=request.POST, partial=True)
            if srz_data.is_valid():
                srz_data.save()
                return Response(srz_data.data, status=status.HTTP_200_OK)
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response('edit label permission denied')

    def destroy(self, request: Response, pk):
        label = get_object_or_404(self.queryset, pk=pk)
        if label.card.cmembershipmodel_set.filter(to_user=request.user).exists()\
        or label.card.list.board.owner == request.user:
            label.delete()
            return Response({'message': 'label deleted'}, status=status.HTTP_200_OK)
        else:
            Response('delete label permission denied')
