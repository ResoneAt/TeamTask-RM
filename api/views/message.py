from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MessageModel
from .serializers import MessageSerializer

class MessagesListAPIView(APIView):
    def get(self, request):
        message = MessageModel.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)



class SendMessageAPIView(APIView):
    def get(self):
        ...

    def post(self):
        ...

    def delete(self):
        ...

    def patch(self):
        ...
