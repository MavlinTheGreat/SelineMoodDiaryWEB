from django.contrib import admin

from .emotionnotes import EmotionNote
from .emotions import Emotion
from .notetags import NoteTag

admin.site.register(Emotion)
admin.site.register(NoteTag)
admin.site.register(EmotionNote)