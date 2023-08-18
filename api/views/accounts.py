from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from api.serializers.accounts import UserSerializers


class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        srz_data = UserSerializers(instance=users, many=True)
        return Response(data=srz_data.data)

