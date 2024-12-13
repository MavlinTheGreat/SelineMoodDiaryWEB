from rest_framework import serializers
from .emotions import Emotion
from .emotionnotes import EmotionNote


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name', 'description', 'rating', 'imageIcon', 'owner', 'is_global']


class EmotionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionNote
        fields = ['id', 'date', 'emotion', 'content', 'user', 'tags']