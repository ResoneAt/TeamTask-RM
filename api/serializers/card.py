from rest_framework import serializers
from tasks.models import ListModel,LabelModel,SubTaskModel

class CardSerializer(serializers.ModelSerializer):
    ...


class SubCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTaskModel
        exclude = ('card',)


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListModel
        exclude = ('board',)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelModel
        exclude = ('card',)

