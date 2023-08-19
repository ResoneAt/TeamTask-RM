from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from api.serializers.accounts import UserSerializers


class SignUpAPIView(APIView):
    def post(self, request):
        ...


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
