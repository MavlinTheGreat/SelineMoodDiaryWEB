# Generated by Django 5.1.2 on 2024-12-08 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diaryuser',
            name='nickname',
        ),
    ]