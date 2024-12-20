from datetime import timedelta, datetime, date
from random import random

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import io
import requests
from PIL import Image

from django.http import HttpResponse
from django.db import models
import matplotlib.dates as mdates
from matplotlib.colors import to_rgba
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from emotionjournal.emotions import Emotion, GROUP_ICONS
from emotionjournal.emotionnotes import EmotionNote

matplotlib.use("Agg")

# для отображения сколько дней подряд пользователь вносит заметки
class UserStrikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # текущий пользователь
        today = date.today()
        #print(today)

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

# затемняет цвет на указанный процент в виде десятичной дроби
# например, при amount=0.10 цвет color затемняется на 10%
def darken_color(color, amount=0.10):
    rgba = to_rgba(color)
    darker_rgba = [(channel * (1 - amount)) if i < 3 else channel for i, channel in enumerate(rgba)]
    return tuple(darker_rgba)


class MoodCategoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(selfself, request):
        user = request.user  # текущий пользователь
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Обработка дат
        try:
            if start_date:
                start_date = pd.to_datetime(start_date).date()

            if end_date:
                end_date = pd.to_datetime(end_date).date()
            else:
                end_date = date.today()
            if not start_date:
                start_date = end_date - timedelta(days=30) # стандартно рассматривается последний месяц (30 дней..)

        except ValueError:
            raise ValidationError("Некорректный формат дат. Используйте формат YYYY-MM-DD.")

        if start_date > end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

        # Фильтрация записей
        notes = EmotionNote.objects.filter(
            user=user,
            date__date__range=(start_date, end_date)
        )

        # Подготовка данных
        group_data = notes.values("emotion__group").annotate(count=models.Count('id'))
        emotion_data = notes.values("emotion__name", "emotion__group").annotate(count=models.Count('id'))

        if not group_data.exists() or not emotion_data.exists():
            return Response({"details": "записей нет, нам конец."})

        # Подготовка данных для круговой диаграммы
        group_df = pd.DataFrame(list(group_data))
        emotion_df = pd.DataFrame(list(emotion_data))
        # Сортировка данных для внешнего круга
        emotion_df_sorted = emotion_df.sort_values(by='emotion__group')
        # Внутренний круг (группы эмоций)
        group_labels = group_df['emotion__group'].tolist()
        # print(group_labels)
        group_colors = [darken_color(GROUP_ICONS.get(group, GROUP_ICONS['OTH'])[1], amount=0.15) for group in group_labels]
        #print(group_colors)
        group_counts = group_df['count'].tolist()

        # Внешний круг (конкретные эмоции)
        emotion_labels = emotion_df_sorted['emotion__name'].tolist()
        # print(emotion_labels)
        emotion_colors = [GROUP_ICONS.get(row['emotion__group'], GROUP_ICONS['OTH'])[1] for _, row in
                          emotion_df_sorted.iterrows()]
        emotion_counts = emotion_df_sorted['count'].tolist()
        # Построение диаграммы
        fig, ax = plt.subplots(figsize=(11, 10))
        size = 0.5  # Ширина кольца
        gap = 0.0025 # зазор
        # случайный угол начала. по идее figsize хватает на любые углы, но так выглядит приятнее всего по опыту
        start_angle = random.randint(0, 91)
        fig.subplots_adjust(top=0.8)

        # font = {'family': 'normal',
        #         'weight': 'bold',
        #         'size': 72}
        # matplotlib.rc('font', **font)

        # Внутренний круг
        wedges1, texts1, _ = ax.pie(
            group_counts,
            radius=1 - size - gap,
            labels=[Emotion.EmotionGroup(code).label for code in group_labels],
            colors=group_colors,
            startangle=start_angle,
            wedgeprops=dict(width=size, edgecolor='w'),
            autopct='%1.1f%%', # одна цифра после запятой
            labeldistance=None, # вырезание подписей
            textprops={'fontsize': 14, 'fontweight': 'bold'}
        )

        # Внешний круг
        wedges2, texts2 = ax.pie(
            emotion_counts,
            radius=1,
            labels=emotion_labels,
            colors=emotion_colors,
            startangle=start_angle,
            wedgeprops=dict(width=size, edgecolor='w'),
            textprops={'fontsize': 14, 'fontweight': 'bold'}
        )

        # Настройки отображения
        ax.axis('equal')  # Сделать круг
        ax.set_title(f"Распределение настроений с {start_date.strftime("%d.%m.%Y")} по {end_date.strftime("%d.%m.%Y")}", fontdict={
            'fontsize': 16,
        }, y=1.1) # заголовок графика

        # ax.legend(wedges1, [Emotion.EmotionGroup(code).label for code in group_labels], title="Группы",
        #           loc="center left", bbox_to_anchor=(0.8, 0.5, 1, 1),
        #           fontsize=14)

        # Сохранение изображения в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Возвращаем картинку как HTTP-ответ
        return HttpResponse(buf, content_type='image/png')
