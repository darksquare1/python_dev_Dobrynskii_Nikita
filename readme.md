# Описание
Веб приложение, которое отдает данные по двум ендпоинтам. Первый ендпоинт отдает информацию о постах, которые пользователь
комментировал, а так же количество комментариев к этим постам. Второй отдает общую информацию о действия пользователя.

# Запуск
## Без докера
Сервис доступен по следующему адресу: https://darksquare1-python-dev-dobrynskii-nikita-9fff.twc1.net, документация доступна на 
https://darksquare1-python-dev-dobrynskii-nikita-9fff.twc1.net/docs, таблицы заполнены данными из app/db/fixtures.py, существующие 
юзеры: user1, user2, user3

## С докером
Перейдите в корень проекта, где лежит Dockerfile. Сбилдите образ командой:

```docker build . -t sqlitefastapi```

Далее для создания и запуска контейнера введите:

```docker run -d -p 8000:8000 --name logs_general sqlitefastapi```

После того как контейнер будет создан обязательно запустите фикстуры:

```docker exec logs_general python -m app.db.fixtures```

Для запуска тестов введите:

```docker exec logs_general python -m pytest```

Документация будет доступна по адресу http://localhost:8000/