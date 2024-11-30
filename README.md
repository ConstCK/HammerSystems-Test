BackEnd:

Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/HammerSystems-Test.git
Перейдите в папку проекта
В терминале создайте виртуальное окружение (например python -m venv venv) и активируйте его (venv\scripts\activate)
Установите все зависимости при помощи pip install -r requirements.txt
Создайте файл .env в каталоге проекта и пропишите в нем настройки по примеру .env.example
Например ключ для Django можно сгенерировать по пути https://realorangeone.github.io/django-secret-key-generator/
или в консоли при помощи "from django.core.management.utils import get_random_secret_key
get_random_secret_key()"
Запустите сервер из каталога проекта (python manage.py runserver)
Важно: На ПК должен быть установлен Docker Desktop для запуска в контейнере

EndPoints:
http://127.0.0.1:8000/admin/ - Доступ к панели администрирования. Используйте admin для имени и пароля.
http://127.0.0.1:8000/api/v1/auth/ - Аутентификация (post запрос с телом по типу 
{"phone_number": "+79181234567"})
http://127.0.0.1:8000/api/v1/login/ - Авторизация (post запрос с телом по типу 
{"pass_code": "7421"})
http://127.0.0.1:8000/api/v1/activate/ - Использование invite code (post запрос с телом по типу 
{"pass_code": "8183", "invite_code": "XuyqaY"})
http://127.0.0.1:8000/api/v1/profile/ - Получение данных профиля (post запрос с телом по типу 
{"pass_code": "8183"})
http://127.0.0.1:8000/schema/swagger-ui/ - Получение Swagger документации. 
http://127.0.0.1:8000/schema/redoc/ - Получение Swagger документации в redoc формате. 




