from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import MessageModel , User
from rest_framework import status
from api.serializers.message import MessagesSerializer


class MessagesListAPIView(APIView):

    def get(self, request):
        user = request.user
        sent_users = MessageModel.objects.filter(sent_messages__to_user=user).distinct()
        received_users = MessageModel.objects.filter(received_messages__from_user=user).distinct()
        chatted_users = (sent_users | received_users).exclude(id=user.id)
        return Response([{'id': user.id, 'username': user.username} for user in chatted_users])

    
    def post(self, request):
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class SendMessageAPIView(APIView):
    def get(self, request, format=None):
        message = MessageModel.objects.all()
        serializer = MessagesSerializer(message, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, format=None):
        message = MessageModel.objects.get(pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
    def patch(self, request, pk):
        message = MessageModel.objects.get(pk=pk)
        serializer = MessagesSerializer(message,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(code=201, data=serializer.data)
        return Response(code=400, data="wrong parameters")
    
        
