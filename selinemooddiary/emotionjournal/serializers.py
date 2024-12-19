from rest_framework import serializers
from .emotions import Emotion
from .emotionnotes import EmotionNote
from .notetags import NoteTag


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name', 'description', 'rating', 'imageIcon', 'owner']

    def validate_owner(self, value):
        # Запрещаем изменение поля owner
        if self.instance and self.instance.owner != value:
            raise serializers.ValidationError("Изменение владельца запрещено.")
        return value


class NotetagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = ['id', 'name', 'desc', 'icon', 'owner']

    def validate_owner(self, value):
        # Запрещаем изменение поля owner
        if self.instance and self.instance.owner != value:
            raise serializers.ValidationError("Изменение владельца запрещено.")
        return value

class EmotionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionNote
        fields = ['id', 'date', 'emotion', 'content', 'user', 'tags']

    def validate_owner(self, value):
        # Запрещаем изменение поля user
        if self.instance and self.instance.user != value:
            raise serializers.ValidationError("Изменение владельца запрещено.")
        return value