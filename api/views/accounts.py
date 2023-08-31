from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, NotificationModel
from ..serializers.accounts import (
    SignUpSerializer,
    UserSerializer,
    NotificationSerializer
)


class SignUpAPIView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        srz_data = SignUpSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.create(validated_data=srz_data.validated_data)
            return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def list(self, request: Request):
        if request.query_params:
            self.queryset = self.queryset.filter(username__icontains=request.query_params['search'])
        srz_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk=None):
        user = get_object_or_404(User, pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not owner'})
        srz_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not owner'})
        user.delete()
        return Response({'message': 'user deleted'}, status=status.HTTP_200_OK)


class NotificationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'pk'

    def list(self, request: Request):
        notifications = NotificationModel.objects.filter(user=request.user)
        srz_data = NotificationSerializer(instance=notifications, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: int=None):
        notification = get_object_or_404(NotificationSerializer, pk=pk)
        srz_data = NotificationSerializer(instance=notification)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: int=None):
        notification = get_object_or_404(NotificationSerializer, pk=pk)
        notification.delete()
        return Response({'message': 'notification deleted'})


class ResetPasswordAPIView(APIView):
    ...
