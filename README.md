# foodgram-project-react
![](https://img.shields.io/badge/Python-3.7.0-blue) 
![](https://img.shields.io/badge/Django-4.2.4-orange)
![](https://img.shields.io/badge/DjangoRestFramework-3.14.0-red)
![](https://img.shields.io/badge/Gunicorn-20.1.0-blue)
![](https://img.shields.io/badge/-Nginx-464646??style=flat-square&amp;logo=NGINX)
![](https://img.shields.io/badge/-Docker-464646??style=flat-square&amp;logo=docker)

## Описание
«Продуктовый помощник» (Проект Яндекс.Практикум)
Сайт является - базой кулинарных рецептов. Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате. Используется docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx.

Сайт: https://foodgram.fun-boom.ru/

## Главная страница
Содержимое главной страницы — список первых шести рецептов, 
отсортированных по дате публикации (от новых к старым).
Остальные рецепты доступны на следующих страницах: 
внизу страницы есть пагинация.

## Страница рецепта
На странице — полное описание рецепта. 
Для авторизованных пользователей — возможность добавить рецепт в избранное и в 
список покупок, возможность подписаться на автора рецепта.

## Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем 
и возможность подписаться на пользователя.

## Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. 
Страница подписок доступна только владельцу.
### Сценарий поведения пользователя:
- Пользователь переходит на страницу другого пользователя или на страницу рецепта
и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
- Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, 
опубликованных теми авторами, на которых он подписался. 
- Сортировка записей — по дате публикации (от новых к старым).
- При необходимости пользователь может отказаться от подписки на автора: 
переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

## Список избранного
Работа со списком избранного доступна только авторизованному пользователю. 
Список избранного может просматривать только его владелец.
### Сценарий поведения пользователя:
- Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
- Пользователь переходит на страницу «Список избранного» и 
просматривает персональный список избранных рецептов.
- При необходимости пользователь может удалить рецепт из избранного.

## Список покупок
Работа со списком покупок доступна авторизованным пользователям. 
Список покупок может просматривать только его владелец.
### Сценарий поведения пользователя:
- Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
- Пользователь переходит на страницу Список покупок, 
там доступны все добавленные в список рецепты. 
- Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем 
и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
- При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в формате .txt.


### Как запустить в ручном режиме
Скачать файл на сервер 
```
https://github.com/FULLLIFE4rever/foodgram-project-react/blob/master/infra/docker-compose.yml
```

Создать файл .env в папке с этим фалом
```
POSTGRES_USER={{ Пользователь БД }}
POSTGRES_PASSWORD={{ Пароль пользователя БД }}
POSTGRES_DB={{ Имя базы данных }}
DB_HOST={{ Имя хоста }}
DB_PORT={{ Порт БД }}
DB_NAME={{ Имя БД }}
SECRET_KEY={{ Серетный ключ Django }}
DEBUG={{ Нужен ли DEBUG в Django }}
ALLOWED_HOSTS={{ Разрешенные имена для Django }}
```

Запустить
```
sudo docker compose up -d
```

Выполнить миграции
```
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
```

Запустить заполнение БД ингредиентами и тегами
```
sudo docker compose -f docker-compose.yml exec backend python manage.py load_ingredients
```

Запустить сбор статики для NGINX
```
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /static/static/
```

### Как запустить в автоматическом режиме

Скопируйте проект к себе git

Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY       # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ сервера

DEBUG                   # Просмотр в Debug режиме Django
ALLOWED_HOSTS           # Разрешенные IP для Django [localhost, 127.0.0.1, доменное имя ]
DB_NAME                 # postgres
POSTGRES_USER           # Postgres пользователь
POSTGRES_PASSWORD       # Postgres пароль
POSTGRES_DB             # Postgres имя БД
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```

# Примеры запросов

**GET**: http://127.0.0.1:8000/api/users/  
Пример ответа:
```json
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/users/?page=4",
  "previous": "http://127.0.0.1:8000/api/users/?page=2",
  "results": [
    {
      "email": "testuser@yandex.ru",
      "id": 0,
      "username": "test.user",
      "first_name": "Test",
      "last_name": "User",
      "is_subscribed": false
    }
  ]
}
```

**POST**: http://127.0.0.1:8000/api/users/  
Тело запроса:
```json
{
  "email": "testuser@yandex.ru",
  "username": "test.user",
  "first_name": "Test",
  "last_name": "User",
  "password": "Qwerty123"
}
```
Пример ответа:
```json
{
"email": "testuser@yandex.ru",
"id": 0,
"username": "test.user",
"first_name": "Test",
"last_name": "User"
}
```

**GET**: http://127.0.0.1:8000/api/recipes/  
Пример ответа:
```json
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/recipes/?page=4",
  "previous": "http://127.0.0.1:8000/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "testuser@yandex.ru",
        "id": 0,
        "username": "test.user",
        "first_name": "Test",
        "last_name": "User",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://127.0.0.1:8000/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

### Об авторе

'''
Александр Зубарев
'''
