from datetime import timedelta, date

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from emotionjournal.emotionnotes import EmotionNote

class UserStrikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # текущий пользователь
        today = date.today()

        # Получаем все заметки пользователя, отсортированные по дате
        notes = (
            EmotionNote.objects.filter(user=user)
            .order_by('date')
            .values_list('date', flat=True)
        )

        if not notes:
            return Response({'strike': 0})  # Если записей нет, возвращаем 0

        # Проверяем наличие заметки за сегодня
        if not any(note.date() == today for note in notes):
            return Response({'strike': 0})  # Если сегодня нет записи, возвращаем 0

        # Инициализируем "страйк" начиная с текущего дня
        strike = 1
        prev_date = today

        # Идем в обратном порядке по записям
        for note_date in reversed(notes):
            note_date = note_date.date()
            if note_date == prev_date - timedelta(days=1):
                strike += 1
                prev_date = note_date
            elif note_date < prev_date - timedelta(days=1):
                break  # Прерываем, если нашли разрыв

        return Response({'strike': strike})


