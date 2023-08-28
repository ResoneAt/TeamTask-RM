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

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        cards = CardModel.objects.filter(cmembership__user=user)
        self.check_object_permissions(request, cards)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CardsAPIView(APIView):
    permission_classes = [IsBoardMember,]

    def get(self, request, board_id):
        query_set = CardModel.objects.filter(list__board_id=board_id)
        board = get_object_or_404(BoardModel, id=board_id)
        self.check_object_permissions(request, board)
        srz_data = CardSerializer(instance=query_set, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CardAPIView(APIView):
    permission_classes = [IsBoardMember,]

    def get(self, request, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        self.check_object_permissions(request, card.list.board)
        srz_data = CardSerializer(instance=card)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CardCreateAPIView(APIView):
    permission_classes = [IsBoardOwner,]

    def post(self, request, list_id):
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

    def put(self, request, card_id):
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

    def delete(self, request, card_id):
        card = get_object_or_404(CardModel, id=card_id)
        self.check_object_permissions(request, card.list.board)
        card.delete()
        return Response({'message': 'card deleted'}, status=status.HTTP_200_OK)


class SubCardViewSet(ViewSet):
    queryset = SubTaskModel.objects.all()

    def create(self, request, card_id):
        if request.user.is_authenticated:
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
        else:
            Response('you have to login first')

    def partial_update(self, request, pk=None):
        if request.user.is_authenticated:
            subcard = get_object_or_404(self.queryset, pk=pk)
            if subcard.card.cmembershipmodel_set.filter(to_user=request.user).exists():
                srz_data = SubCardSerializer(instance=subcard, data=request.POST, partial=True)
                if srz_data.is_valid():
                    srz_data.save()
                    return Response(srz_data.data, status=status.HTTP_200_OK)
                return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                Response('permission denied, you are not a member of this card')
        else:
            Response('you have to login first')

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            subcard = get_object_or_404(self.queryset, pk=pk)
            if subcard.card.cmembershipmodel_set.filter(to_user=request.user).exists():
                subcard.delete()
                return Response({'message': 'subcard deleted'}, status=status.HTTP_200_OK)
            else:
                Response('permission denied, you are not a member of this card')
        else:
            Response('you have to login first')


class ListViewSet(ViewSet):
    queryset = ListModel.objects.all()

    def create(self, request, board_id):
        if request.user.is_authenticated:
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
        else:
            Response('you have to login first')

    def partial_update(self, request, pk=None):
        if request.user.is_authenticated:
            list = get_object_or_404(self.queryset, pk=pk)
            if list.board.owner == request.user:
                srz_data = ListSerializer(instance=list, data=request.POST, partial=True)
                if srz_data.is_valid():
                    srz_data.save()
                    return Response(srz_data.data, status=status.HTTP_200_OK)
                return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                Response('permission denied, you are not board owner')
        else:
            Response('you have to login first')

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            list = get_object_or_404(self.queryset, pk=pk)
            if list.board.owner == request.user:
                list.delete()
                return Response({'message': 'list deleted'}, status=status.HTTP_200_OK)
            else:
                Response('permission denied, you are not board owner')
        else:
            Response('you have to login first')


class LabelViewSet(ViewSet):
    queryset = LabelModel.objects.all()

    def create(self, request, card_id):
        if request.user.is_authenticated:
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
        else:
            Response('you have to login first')

    def partial_update(self, request, pk=None):
        if request.user.is_authenticated:
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
        else:
            Response('you have to login first')

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            label = get_object_or_404(self.queryset, pk=pk)
            if label.card.cmembershipmodel_set.filter(to_user=request.user).exists()\
                    or label.card.list.board.owner == request.user:
                label.delete()
                return Response({'message': 'label deleted'}, status=status.HTTP_200_OK)
            else:
                Response('delete label permission denied')
        else:
            Response('you have to login first')
