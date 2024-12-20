# Selin Mood Diary - трекер настроения!

## Что за проект?
Это учебный проект по дисциплине "Web-программирование" на 3-м курсе программы "Фундаментальное программирование и информационые технологии: инженерия разработки программного обеспечения".

Представляет собой начальную версию веб-приложения для психологического самоконтроля и ведения заметок с **отметками** настроения.

Язык бэкенда - Python, библиотека Python Django, используется Djangorestframework, matplotlib, seaborn и другие.

Язык фронтенда - Javascript (Node JS), используется библиотека React, пакеты Axios и некоторые другие. 

## Запуск программы
Выбрать папку загрузки. В ней командной строке/терминале выполнить:
```git
git clone https://github.com/MavlinTheGreat/SelineMoodDiaryWEB
cd SelineMoodDiaryWEB
cd selinemooddiary
docker-compose down --volumes && docker-compose up --build
```
Далее веб-интерфейс приложения должен быть доступен по адресу *localhost:3000*. По адресу *localhost:8000/api/* располагаются разнообразные API, используемые фронтендом.

## Разработчики
Разработку проекта осуществляли следующие студенты группы БФИ2202:

-Никитин Павел Михайлович

-Карзанов Василий Васильевич

-Шубина Мария Алексеева

-Крюкова Диана Романовна
