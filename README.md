# Django Stock Manager
## Общее описание:
Приложение, позволяющее регистрировать сделки покупки/продажи ценных бумаг
## Стек:
* Python 3.11
* Django 4+
* DjangoRestFramework
* PostgreSQL
* Docker
* Celery, Celery-beat
* Redis
* SimpleJWT
* django-silk

## Настройка и запуск проекта
1. склонировать проект:
```
git clone https://github.com/demetrzz/django-stock-manager.git
```
2. создать файл .env в корне проекта по примеру:
```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_DB=db
POSTGRES_DB=stock_manager
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
DB_PORT=5432
DEBUG=True
ALLOWED_HOSTS=0.0.0.0 127.0.0.1 localhost [::1]
SECRET_KEY=your_key
```
3. создать и запустить контейнеры:
```
docker compose build
docker compose up
```
Во время запуска, помимо runserver, создадутся миграции, выполнятся тесты (код полностью покрыт тестами), сколлектятся статик файлы, это действия также можно выполнить вручную, подключившись к контейнеру:
```
python manage.py makemigrations
python manage.py test
python manage.py collectstatic  --noinput
```

4. подключиться к контейнеру web в докере:
```
docker exec -t -i container_id sh
```
5. провести миграции:
```
python manage.py migrate
```
6. наполнить базу актуальными данными с REST API МосБиржи:
```
python manage.py db_data_initialization
```
7. создать супер юзера:
```
python manage.py createsuperuser
```
8. По необходимости, после настройки, перезапустить контейнеры:
```
docker compose down
docker compose up
```

## Реализованный функционал:
* Эндпоинты с CRUD операциями
* Авторизация и аутентификация посредством JWT токена
* Асинхронное обновление базы данных ценных инструментов (фоновые задачи) с использованием Celery-beat
* Кэширование данных на BondsViewSet для снятия нагрузки на сервер, возможность оптимизации SQL-запросов с помощью django-silk
* Код покрыт юнит-тестами
* Интеграция с RESTful API Московской биржи, возможность представить обработанные (отобранные по параметрам и подходящим критериям) данные

## Документация по эндпоинтам:
1. **api/v1/token/** : POST при вводе валидных логине и пароле возвращает JWT токен для аутентификации и refresh токен ![img_4.png](https://i.imgur.com/3qpHbYn.png)
2. **api/v1/token/refresh/** : POST При предоставлении refresh токена, возвращает обновленный JWT токен для аутентификации ![img_5.png](https://i.imgur.com/8cslGYA.png)
3. **silk/** : GET Доступ к интерфейсу django-silk для просмотра выполненных SQL-запросов ![img_3.png](https://i.imgur.com/X2KTp2c.png)
4. **api/v1/deals/** :
* GET возвращает список (или конкретную сделку с указанным в url id) сделок авторизованного юзера ![img_7.png](https://i.imgur.com/vNboQeO.png)
* POST/PUT/PATCH добавляет/изменяет сделку авторизованного юзера, принимает параметры в теле запроса - buy: bool, quantity: int, bonds: int ![img_6.png](https://i.imgur.com/1TOOFnC.png)
* DELETE удаляет сделку по указанному в url id ![img_8.png](https://i.imgur.com/sFCD6ZB.png)
5. **api/v1/bonds/** : GET возвращает список всех ценных бумаг в базе данных ![img_2.png](https://i.imgur.com/KAJ1o1e.png)
