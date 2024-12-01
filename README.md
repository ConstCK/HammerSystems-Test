Тестовое задание для Hammer Systems. Приложение для авторизации по номеру телефона.
Используемый стек: Django, DRF, Postgresql (sqlite3 на pythonanywhere.com), SCSS, Docker

* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/HammerSystems-Test.git
* Перейдите в папку проекта
* В терминале создайте виртуальное окружение (например python -m venv venv) и активируйте его (venv\scripts\activate)
* Установите все зависимости при помощи pip install -r requirements.txt
* Создайте файл .env в каталоге проекта и пропишите в нем настройки по примеру .env.example
* Например ключ для Django можно сгенерировать по пути https://realorangeone.github.io/django-secret-key-generator/
или в python консоли при помощи "from django.core.management.utils import get_random_secret_key,
get_random_secret_key()"

**_Запустите сервер из каталога проекта (python manage.py runserver)_**

## Важно: На ПК должен быть установлен Docker Desktop **для запуска в контейнере**

1. Запустите Docker Desktop на пк В консоли из каталога проекта
2. Запустите "docker-compose up" для запуска в контейнере

EndPoints:

### Запуск в контейнере:

http://localhost:8080/ - Доступ к администрированию БД. Используйте при запуске
в Docker контейнере.

### Запуск на локальном сервере или в контейнере:

* http://localhost:8000/accounts/auth/ - Аутентификация с вводом номера телефона
формата: +12345678900
* http://localhost:8000/accounts/login/ - Авторизация с вводом 4-значного pass code с переходом 
на страницу профиля

* http://localhost:8000/admin/ - Доступ к панели администрирования.
Используйте admin для имени и пароля.
* http://localhost:8000/api/v1/auth/ - Аутентификация (post запрос с телом по типу 
{"phone_number": "+79181234567"})
* http://localhost:8000/api/v1/login/ - Авторизация (post запрос с телом по типу 
{"pass_code": "7421"})
* http://localhost:8000/api/v1/activate/ - Использование invite code (post запрос с телом по типу 
{"pass_code": "8183", "invite_code": "XuyqaY"})
* http://localhost:8000/api/v1/profile/ - Получение данных профиля (post запрос с телом по типу 
{"pass_code": "8183"})
* http://localhost:8000/schema/swagger-ui/ - Получение Swagger документации. 
* http://localhost:8000/schema/redoc/ - Получение Swagger документации в redoc формате. 

### Запуск на pythonanywhere.com:
* http://ConstKK.pythonanywhere.com/accounts/auth/ - Аутентификация с вводом номера телефона
формата: +12345678900
* http://ConstKK.pythonanywhere.com/accounts/login/ - Авторизация с вводом 4-значного pass code с переходом 
на страницу профиля
* http://ConstKK.pythonanywhere.com/admin/ - Доступ к панели администрирования.
Используйте admin для имени и пароля.
* http://ConstKK.pythonanywhere.com/api/v1/auth/ - Аутентификация (post запрос с телом по типу 
{"phone_number": "+79181234567"})
* http://ConstKK.pythonanywhere.com/api/v1/login/ - Авторизация (post запрос с телом по типу 
{"pass_code": "7421"})
* http://ConstKK.pythonanywhere.com/api/v1/activate/ - Использование invite code (post запрос с телом по типу 
{"pass_code": "8183", "invite_code": "XuyqaY"})
* http://ConstKK.pythonanywhere.com/api/v1/profile/ - Получение данных профиля (post запрос с телом по типу 
{"pass_code": "8183"})
* http://ConstKK.pythonanywhere.com/schema/swagger-ui/ - Получение Swagger документации. 
* http://ConstKK.pythonanywhere.com/schema/redoc/ - Получение Swagger документации в redoc формате. 

