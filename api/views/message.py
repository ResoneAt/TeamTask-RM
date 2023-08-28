from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import MessageModel , User
from rest_framework import status
from api.serializers.message import MessagesSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class MessagesListAPIView(APIView):
    serializer_class = MessagesSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        View the list of users who messaged me.
        Requires the 'to_user' and 'from_user' and 'user_id' parameter.
        Returns the user list.
        """
        user = request.user
        sent_users = MessageModel.objects.filter(pv_sender__to_user=user).distinct()
        received_users = MessageModel.objects.filter(receiver__from_user=user).distinct()
        chatted_users = (sent_users | received_users).exclude(id=user.id)
        return Response([{'id': user.id, 'username': user.username} for user in chatted_users])

    def post(self, request):
        """
        Create and view a user list.
        Returns the created user list.
        """
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SendMessageAPIView(APIView):
    serializer_class = MessagesSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, message_id):
        """
        Retrieve a specific message by its ID.
        Requires the 'message_id' parameter.
        Returns the message details.
        """
        message = get_object_or_404(MessageModel, id=message_id)
        serializer = MessagesSerializer(message)
        return Response(serializer.data)

    def post(self, request):
        """
        Create and send a new message.
        Requires 'receiver_id' and 'text' fields in the request data.
        Returns the created message.
        """
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
        """
        Delete a specific message by its ID.
        Requires the 'message_id' parameter.
        The authenticated user can only delete their own messages.
        Returns a success message upon successful deletion.
        """
        message = get_object_or_404(MessageModel, id=message_id)

        if message.from_user != request.user:
            return Response({'error': 'You do not have permission to delete this message.'},
                            status=status.HTTP_403_FORBIDDEN)

        message.delete()
        return Response({'message': 'Message deleted successfully.'})

    def patch(self, request, message_id):
        """
        Update a specific message by its ID.
        Requires the 'message_id' parameter.
        The authenticated user can only update their own messages.
        Returns the updated message.
        """
        message = get_object_or_404(MessageModel, id=message_id)

        if message.sender != request.user:
            return Response({'error': 'You do not have permission to update this message.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = MessagesSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
