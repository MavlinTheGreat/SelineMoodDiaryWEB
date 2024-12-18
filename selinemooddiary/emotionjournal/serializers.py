from rest_framework import serializers
from .emotions import Emotion
from .emotionnotes import EmotionNote
from .notetags import NoteTag


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name', 'description', 'rating', 'imageIcon', 'owner']


class NotetagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = ['id', 'name', 'desc', 'icon', 'owner']


class EmotionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionNote
        fields = ['id', 'date', 'emotion', 'content', 'user', 'tags']