from datetime import timedelta, date
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

from django.http import HttpResponse
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from emotionjournal.emotionnotes import EmotionNote

# для отображения сколько дней подряд пользователь вносит заметки
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


class MoodGraphView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # текущий пользователь
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Обработка дат
        try:
            if start_date:
                start_date = pd.to_datetime(start_date).date()
            else:
                start_date = now().date() - timedelta(days=7)  # последняя неделя

            if end_date:
                end_date = pd.to_datetime(end_date).date()
            else:
                end_date = now().date()
        except ValueError:
            raise ValidationError("Некорректный формат дат. Используйте формат YYYY-MM-DD.")

        if start_date > end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

        # Фильтрация записей
        notes = EmotionNote.objects.filter(
            user=user,
            date__date__range=(start_date, end_date)
        ).select_related('emotion')

        if not notes.exists():
            return Response({"detail": "Нет записей за указанный период."})

        # Преобразуем данные в DataFrame
        data = [
            {
                "date": note.date.date(),
                "rating": note.emotion.rating if note.emotion else None
            }
            for note in notes
        ]
        df = pd.DataFrame(data).dropna()  # Убираем записи без рейтинга

        # Группируем по дате и рассчитываем средний рейтинг
        daily_ratings = df.groupby("date")["rating"].mean().reset_index()

        # Построение графика
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=daily_ratings, x="date", y="rating", marker="o")
        plt.title("Колебания настроения")
        plt.xlabel("Дата")
        plt.ylabel("Средний рейтинг")
        plt.xticks(rotation=45)

        # Сохранение графика в буфер
        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        # Возвращаем график как HTTP-ответ
        return HttpResponse(buffer, content_type="image/png")