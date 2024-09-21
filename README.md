# Yatube API Documentation

Yatube API предоставляет доступ к социальной сети Yatube, позволяя пользователям:
- Подписываться друг на друга
- Создавать посты
- Комментировать посты

Этот API поддерживает аутентификацию через JWT-токены.

Технологии:
- Python 3.8+
- Django 3.2
- Django REST Framework
- Simple JWT

Для начала использования выполните следующие шаги:

# Установка Yatube API

def install_instructions():

1. Клонируйте репозиторий:
```
    git clone <ссылка на репозиторий>
```
2. Перейдите в директорию проекта:
```
    cd api_final_yatube
```
3. Установите виртуальное окружение и активируйте его:

   Для Linux и MacOS:
```
       python -m venv venv
       source venv/bin/activate
```
   Для Windows:
```
       python -m venv venv
       venv\Scripts\activate
```
   4. Установите зависимости:
```
       pip install -r requirements.txt
```
   5. Выполните миграции:
```
       python manage.py migrate
```
   6. Запустите сервер:
```
       python manage.py runserver
```

# Аутентификация в API

def authentication_instructions():

Для доступа к защищённым эндпоинтам API необходимо использовать JWT-токены.

1. Чтобы получить JWT-токен, выполните POST-запрос:
```
        POST /api/v1/jwt/create/
```
Тело запроса (JSON):
```
    {
        "username": "your_username",
        "password": "your_password"
    }
```
Пример ответа (JSON):
```
    {
        "refresh": "your_refresh_token",
        "access": "your_access_token"
    }
```
2. Используйте токен для доступа к API. Передавайте его в заголовке каждого запроса:
```
        Authorization: Bearer your_access_token
```
3. Для обновления токена выполните запрос:
```
        POST /api/v1/jwt/refresh/
```
Тело запроса (JSON):
```
    {
        "refresh": "your_refresh_token"
    }
```

# Примеры запросов к API

def api_usage_examples():

Публикации:
------------

1. Получение списка публикаций:
```
        GET /api/v1/posts/
```
Параметры:
```
    - limit — количество публикаций на странице.
    - offset — смещение от начала списка.
```
Пример:
```
    GET /api/v1/posts/?limit=10&offset=20
```
2. Создание публикации:
```
    POST /api/v1/posts/
```
Заголовки:
```
    Content-Type: application/json
    Authorization: Bearer your_access_token
```
Тело запроса (JSON):
```
    {
        "text": "Текст новой публикации",
        "group": 1  # ID существующей группы (необязательно)
    }
```
Комментарии:
-------------

1. Получение комментариев к публикации:
```
    GET /api/v1/posts/{post_id}/comments/
```
2. Добавление комментария к публикации:
```
    POST /api/v1/posts/{post_id}/comments/
```
   Заголовки:
```
       Content-Type: application/json
       Authorization: Bearer your_access_token
```
   Тело запроса (JSON):
```
   {
       "text": "Текст комментария"
   }
```
   Подписки:
   ---------

   1. Получение списка подписок:
```
       GET /api/v1/follow/
```
   Заголовки:
```
       Authorization: Bearer your_access_token
```
   2. Создание подписки:
```
       POST /api/v1/follow/
```
   Заголовки:
```
       Content-Type: application/json
       Authorization: Bearer your_access_token
```
   Тело запроса (JSON):
```
   {
       "following": "username"
   }
```
   Примечание: при попытке подписаться на самого себя будет возвращена ошибка.


# Запуск документации API

def api_docs_info():

Подробная документация доступна по адресу:
```
   http://127.0.0.1:8000/redoc/
```
В документации описаны все доступные эндпоинты, методы запросов, параметры и примеры ответов.


# Лицензия

## def license_info():

### Проект распространяется под лицензией MIT.


# Обратная связь

## def feedback_info():

### Если у вас есть вопросы или предложения по улучшению проекта, создайте issue в репозитории или свяжитесь с автором проекта.
