# Pereval REST API

REST API для мобильного приложения туристов Федерации Спортивного Туризма России (ФСТР). Позволяет добавлять, редактировать и просматривать информацию о горных перевалах.

## Описание

API предоставляет возможность:
- Создание перевалов с указанием координат, высоты и названия
- Загрузка нескольких фотографий перевала
- Указание информации о пользователе (имя, почта, телефон)
- Модерация перевалов (новый, в работе, принят, отклонен)
- Просмотр и редактирование данных

## Технологии

- Python 3.13.2
- Django
- Django REST Framework
- PostgreSQL
- drf-writable-nested (для работы с вложенными сериализаторами)

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/smolnikov-ai/NewPereval.git
cd pereval
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
```
Создайте файл .env в корне проекта:
SECRET_KEY=your_secret_key_django
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=your_username
FSTR_DB_PASS=your_password
```

### 5. Настройка базы данных
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Запуск сервера разработки
```bash
python manage.py runserver
```

### Тестирование
Запуск тестов:
```bash
python manage.py test
```

### Модели данных
```
User (Пользователь)
email - Email пользователя
fam - Фамилия
name - Имя
otc - Отчество (необязательно)
phone - Телефон (максимум 12 символов)
Coords (Координаты)
latitude - Широта (от -90 до 90)
longitude - Долгота (от -180 до 180)
height - Высота в метрах
Level (Уровень сложности)
winter - Сложность зимой (1А, 1Б, 2А, 2Б, 3А, 3Б)
summer - Сложность летом (1А, 1Б, 2А, 2Б, 3А, 3Б)
autumn - Сложность осенью (1А, 1Б, 2А, 2Б, 3А, 3Б)
spring - Сложность весной (1А, 1Б, 2А, 2Б, 3А, 3Б)
Pereval (Перевал)
user - Связь с пользователем
coords - Связь с координатами
level - Связь с уровнем сложности
beauty_title - Красивое название (необязательно)
title - Название перевала (обязательно)
other_titles - Другие названия (необязательно)
connect - Связь (необязательно)
add_time - Время добавления (автоматически)
status - Статус модерации (new, pending, accepted, rejected)
Images (Изображения)
data - URL изображения
title - Название изображения
pereval - Связь с перевалом
```

### Получение списка всех перевалов
```
GET /api/pereval/
```

### Создание нового перевала
```
POST /api/pereval/
Content-Type: application/json
```

### Пример запроса:
```
{
    "user": {
        "email": "example@example.com",
        "fam": "Family",
        "name": "Name",
        "otc": "Patronymic",
        "phone": "+79876543210"
    },
    "coords": {
        "latitude": "11.111100",
        "longitude": "22.222200",
        "height": 3333
    },
    "level": {
        "winter": "2А",
        "summer": "1А",
        "autumn": "1Б",
        "spring": "1Б"
    },
    "beauty_title": "Beauty title",
    "title": "New title",
    "other_titles": "Other titles",
    "connect": "",
    "images": [
        {
            "data": "https://example.com/image1.jpg",
            "title": "Подъём"
        },
        {
            "data": "https://example.com/image2.jpg",
            "title": "Седловина"
        }
    ]
}
```

### Получение информации о конкретном перевале
```
GET /api/pereval/{id}/
```

### Обновление информации о перевале
```
PATCH /api/pereval/{id}/
Content-Type: application/json
Важно: Редактирование возможно только для перевалов со статусом "new"
```

### Статусы модерации
```
new - Новый (по умолчанию)
pending - В работе
accepted - Принят
rejected - Отклонен
Уровни сложности
1А - Первая категория, легко
1Б - Первая категория, усложненный
2А - Вторая категория, легко
2Б - Вторая категория, усложненный
3А - Третья категория, легко
3Б - Третья категория, усложненный
Особенности работы
Пользователи - при повторной отправке данных пользователя с тем же email используется существующая запись
Редактирование - возможно только для перевалов в статусе "new"
Изображения - поддерживаются множественные загрузки
Валидация - все поля проходят строгую валидацию
```

### Автор
```
Smolnikov Anton Ivanovich - smolmikov-ai@mail.ru
```


