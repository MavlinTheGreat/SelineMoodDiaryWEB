from django.db import migrations

def add_initial_data(apps, schema_editor):
    Emotion = apps.get_model('emotionjournal', 'Emotion')
    NoteTag = apps.get_model('emotionjournal', 'NoteTag')


    emotions = [
        ('Счастье', 'Состояние эйфории. Солнышко светит ярко, вас переполняют радостные эмоции и вы готовы поделиться ими со всем миром!',
         10, 'STATIC/EMOTION_ICONS/schastie.png', 'HAP'),
        ('Радость',
         'Вы ощущаете себя просто превосходно! =)',
         9, 'STATIC/EMOTION_ICONS/radost.png', 'HAP'),
        ('На подъёме', 'Дела начинают идти в гору, кажется, что вы уверено принимаете вызов от этой жизни!',
         8, 'STATIC/EMOTION_ICONS/na_podeme.png', 'CALM'),
        ('Покой', 'Наконец-то спокойно и нетревожно.',
         7, 'STATIC/EMOTION_ICONS/pokoy.png', 'CALM'),
        ('Безразличие', 'Вам вроде и не плохо, но ничего не вовлекает.',
         6, 'STATIC/EMOTION_ICONS/bezrazlichie.png', 'INDIF'),
        ('Скука', 'Полная апатия.',
         5, 'STATIC/EMOTION_ICONS/skuka.png',  'INDIF'),
        ('Раздражённость', 'Все немного подбешивают, так и норовя попасть под руку! Вы скоро взорвётесь!',
         4, 'STATIC/EMOTION_ICONS/razdrazhennost.png', 'ANG'),
        ('Злость', 'Вы в ярости, и негатив съедает вас изнутри.',
         3, 'STATIC/EMOTION_ICONS/zlost.png', 'ANG'),
        ('Тревога', 'Негатив, страхи настоящего и будущего медленно съедают вас изнутри.',
         2, 'STATIC/EMOTION_ICONS/trevoga.png', 'SAD'),
        ('Грусть', 'Тоска, да и только.',
         1, 'STATIC/EMOTION_ICONS/grust.png', 'SAD'),
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