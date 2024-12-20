from django.db import migrations

def add_initial_data(apps, schema_editor):
    Emotion = apps.get_model('emotionjournal', 'Emotion')
    NoteTag = apps.get_model('emotionjournal', 'NoteTag')


    emotions = [
        ('Счастье', 'Состояние эйфории. Солнышко светит ярко, вас переполняют радостные эмоции и вы готовы поделиться ими со всем миром!',
         10, 'STATIC/EMOTION_ICONS/Green_face.webp', 'HAP'),
        ('Радость',
         'Вы ощущаете себя просто превосходно! =)',
         9, 'STATIC/EMOTION_ICONS/Dance-0.webp', 'HAP'),
        ('Спокойствие', 'Всё хорошо. Вас ничто не тревожит, вы ощущаете жизненный оптимизм.',
         8, 'STATIC/EMOTION_ICONS/Blue_face.webp', 'CALM'),
        ('Расслабленность', 'Вы нормально себя чувствуете.',
         7, 'STATIC/EMOTION_ICONS/Blue_face_1.webp', 'CALM'),
        ('Безразличие', 'Вам вроде и не плохо, но ничего не вовлекает.',
         6, 'STATIC/EMOTION_ICONS/CuriosRelation.webp', 'INDIF'),
        ('Скука', 'Полная апатия.',
         5, 'STATIC/EMOTION_ICONS/Yellow_face.webp',  'INDIF'),
        ('Раздражённость', 'Все немного подбешивают, так и норовя попасть под руку!',
         4, 'STATIC/EMOTION_ICONS/Orange_face.webp', 'ANG'),
        ('Злость', 'Вы в ярости, и негатив съедает вас изнутри.',
         3, 'STATIC/EMOTION_ICONS/Red_face.webp', 'ANG'),
        ('Тревога', 'Негатив, страхи настоящего и будущего медленно съедают вас.',
         2, 'media/STATIC/EMOTION_ICONS/Scared.webp', 'SAD'),
        ('Грусть', 'Тоска, да и только.',
         1, 'STATIC/EMOTION_ICONS/Face_sadness.webp', 'SAD'),
    ]

    for name, description, rating, imagepath, group in emotions:
        Emotion.objects.create(name=name, description=description, rating=rating, imageIcon=imagepath, group=group)

    # Пример начальных данных для тегов
    tags = [
        ('Спорт', 'Были занятия спортом'),
        ('Друзья', 'Провёл время с друзьями'),
        ('Медитация', 'Помедитировал!'),
    ]

    for name, desc in tags:
        NoteTag.objects.create(name=name, desc=desc)

class Migration(migrations.Migration):
    dependencies = [
         ('emotionjournal', '0001_initial'),  # Предположим, что миграция 0001_initial уже существует
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]