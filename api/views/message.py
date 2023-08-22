from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import MessageModel , User
from rest_framework import status
from api.serializers.message import MessagesSerializer
from django.shortcuts import get_object_or_404


class MessagesListAPIView(APIView):

    def get(self, request):
        user = request.user
        sent_users = MessageModel.objects.filter(pv_sender__to_user=user).distinct()
        received_users = MessageModel.objects.filter(receiver__from_user=user).distinct()
        chatted_users = (sent_users | received_users).exclude(id=user.id)
        return Response([{'id': user.id, 'username': user.username} for user in chatted_users])

    
    def post(self, request):
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class SendMessageAPIView(APIView):
    
    def get(self, request, message_id):
        message = get_object_or_404(MessageModel, id=message_id)
        serializer = MessagesSerializer(message)
        return Response(serializer.data)
    
    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        text = request.data.get('text')

        if not receiver_id or not text:
            return Response({'error': 'Please provide receiver_id and text.'}, status=400)

        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found.'}, status=404)

        message = MessageModel.objects.create(sender=sender, receiver=receiver, text=text)
        serializer = MessagesSerializer(message)
        return Response(serializer.data, status=201)

    def delete(self, request, message_id):
        message = get_object_or_404(MessageModel, id=message_id)

        if message.from_user != request.user:
            return Response({'error': 'You do not have permission to delete this message.'}, status=status.HTTP_403_FORBIDDEN)

        message.delete()
        return Response({'message': 'Message deleted successfully.'})
     
     
    def patch(self, request, message_id):
        message = get_object_or_404(MessageModel, id=message_id)

        if message.sender != request.user:
            return Response({'error': 'You do not have permission to update this message.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = MessagesSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
