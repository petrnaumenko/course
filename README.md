# Инструкции по запуску проекта

Данный файл содержит инструкции по клонированию и запуску проекта.

## Клонирование проекта

Для начала необходимо клонировать репозиторий проекта на ваш локальный компьютер. Откройте терминал и выполните следующую команду:

```bash
git clone https://github.com/petrnaumenko/course.git
```

## Настройка и запуск проекта
После клонирования репозитория необходимо перейти в папку проекта, выполнить миграции и запустить сервер разработки.

```bash
cd course
./manage.py migrate
./manage.py runserver
```

## Запуск демонстрационного скрипта
Также в проекте присутствует демонстрационный скрипт, который можно запустить следующим образом. Откройте новую консоль, перейдите в папку проекта и выполните команду:

```bash
./rundemo.py
```
Эта команда запустит демонстрационный скрипт, предназначенный для показа некоторых возможностей проекта.

