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
    def get(self, request, format=None):
        message = MessageModel.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        message = MessageModel.objects.all()
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
    def patch(self, request):
        message = MessageModel.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)
    
        
