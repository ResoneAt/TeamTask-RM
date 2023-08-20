from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MessageModel
from rest_framework import status
from .serializers import MessageSerializer


class MessagesListAPIView(APIView):

    def get(self, request):
        message = MessageModel.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class SendMessageAPIView(APIView):
    def get(self, request, formmat=None):
        message = MessageModel.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)


    def post(self):
        ...

    def delete(self):
        ...

    def patch(self):
        ...
