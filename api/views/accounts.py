from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from ..serializers.accounts import (
    SignUpSerializer,
    UserSerializer,
    NotificationSerializer
)


class SignUpAPIView(APIView):

    def post(self, request):
        srz_data = SignUpSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.create(validated_data=srz_data.validated_data)
            return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        ...


class LogoutAPIView(APIView):
    def post(self, request):
        ...


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    query_set = User.objects.all()

    def list(self, request):
        if request.query_params:
            self.query_set = self.query_set.filter(username__icontains=request.query_params['search'])
        srz_data = UserSerializer(instance=self.query_set, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not owner'})
        srz_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not owner'})
        user.delete()
        return Response({'message': 'user deleted'}, status=status.HTTP_200_OK)


class NotificationViewSet(viewsets.ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...

    def destroy(self, request, pk=None):
        ...


class ResetPasswordAPIView(APIView):
    ...
