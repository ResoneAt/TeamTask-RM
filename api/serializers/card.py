from rest_framework import serializers
from tasks.models import ListModel

class CardSerializer(serializers.ModelSerializer):
    ...


class SubCardSerializer(serializers.ModelSerializer):
    ...


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListModel
        exclude = ('board',)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListModel
        exclude = ('card',)

