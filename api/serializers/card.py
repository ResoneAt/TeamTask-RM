from rest_framework import serializers
from tasks.models import ListModel,LabelModel

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
        model = LabelModel
        exclude = ('card',)

