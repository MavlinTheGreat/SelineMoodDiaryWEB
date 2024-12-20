from datetime import timedelta, datetime, date
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import os
import requests
from PIL import Image

from django.http import HttpResponse
from matplotlib import image as mpimg
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from emotionjournal.emotionnotes import EmotionNote

from selinemooddiary import settings

matplotlib.use("Agg")

# для отображения сколько дней подряд пользователь вносит заметки
class UserStrikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # текущий пользователь
        today = date.today()
        print(today)

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

# график колебаний настроения
class MoodGraphView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # текущий пользователь
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        #print(start_date, end_date)

        # Обработка дат
        try:
            if start_date:
                start_date = pd.to_datetime(start_date).date()

            if end_date:
                end_date = pd.to_datetime(end_date).date()
            else:
                end_date = date.today()
            if not start_date:
                start_date = end_date - timedelta(days=7)

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
            return Response({"detail": "Нет записей"})

        # Преобразуем данные в DataFrame
        data = [
            {
                "date": note.date.date(),
                "rating": note.emotion.rating if note.emotion else None
            }
            for note in notes
        ]
        df = pd.DataFrame(data).dropna()  # Убираем записи без рейтинга

        daycount = pd.to_datetime(df['date'])
        if daycount.dt.date.nunique() < 3:
            return Response({"detail": "Недостаточно записей"})
        else:
            print(df)

        # Группируем по дате и рассчитываем средний рейтинг
        daily_ratings = df.groupby("date")["rating"].mean().reset_index()

        # Преобразуем даты в числовой формат
        daily_ratings['date_num'] = mdates.date2num(daily_ratings['date'])

        # Построение графика
        fig, ax = plt.subplots(figsize=(12, 7))
        sns.lineplot(data=daily_ratings, x="date", y="rating", marker="o", ax=ax)
        plt.subplots_adjust(left=0.25, right=0.95)  # Увеличиваем отступ слева
        ax.set_title("Колебания настроения")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Средний рейтинг")
        plt.xticks(rotation=45)

        # Расширяем границы графика
        ax.set_xlim(daily_ratings['date_num'].iloc[0] - 0.5, daily_ratings['date_num'].iloc[-1] + 0.5)

        # Настройка оси Y с изображениями
        ax.set_yticks(range(1, 11))  # Размещение меток оси Y от 1 до 10
        ax.set_yticklabels([''] * 10)  # Убираем текстовые метки
        ax.yaxis.set_tick_params(pad=30)

        # Загружаем изображение
        pictures = (
            'http://127.0.0.1:8000/media/static/emotion_icons/face_sadness.png',
            '',
            'http://127.0.0.1:8000/media/static/emotion_icons/orange_face.png',
            '',
            'http://127.0.0.1:8000/media/static/emotion_icons/yellow_face.png',
            '',
            '',
            'http://127.0.0.1:8000/media/static/emotion_icons/blue_face.png',
            '',
            'http://127.0.0.1:8000/media/static/emotion_icons/green_face.png'
        )
        # Размещаем изображения слева от оси Y
        for rating in (0, 2, 4, 7, 9):
            icon_url = pictures[rating]
            response = requests.get(icon_url)
            img = Image.open(io.BytesIO(response.content))
            if img:
                img_array = OffsetImage(img, zoom=0.7, alpha=0.6)
            ab = AnnotationBbox(
                img_array,  # Объект изображения
                (daily_ratings['date_num'].iloc[0] - 0.5, rating + 1),  # Смещение координат X (слева от оси)
                frameon=False,  # Без рамки
                boxcoords="data",
                box_alignment=(1.5, 0.5)  # Выравнивание по правому краю изображения
            )
            ax.add_artist(ab)

        # Сохранение графика в буфер
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close('all')

        # Возвращаем график как HTTP-ответ
        return HttpResponse(buffer, content_type="image/png")