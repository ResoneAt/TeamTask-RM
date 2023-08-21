from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from ..serializers.accounts import (
    SignUpSerializer,
    ProfileSerializer,
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


class ProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request, pk=None):
        ...


class NotificationViewSet(viewsets.ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...

    def destroy(self, request, pk=None):
        ...


class ResetPasswordAPIView(APIView):
    ...
