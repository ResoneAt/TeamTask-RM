from rest_framework import serializers
from accounts.models import MessageModel



class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ['from_user', 'to_user', 'text']
        

