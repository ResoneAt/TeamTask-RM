from rest_framework import serializers
from tasks.models import ListModel, LabelModel, SubTaskModel, CardModel


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        exclude = ('list',)


class SubCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTaskModel
        exclude = ('card',)


class ListSerializer(serializers.ModelSerializer):
    cards_count = ...
    class Meta:
        model = ListModel
        exclude = ('board',)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelModel
        exclude = ('card',)
