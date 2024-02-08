#!/bin/bash

SCHEMA="${3:-https}"
HOST="${4:-default}"
USER="${5:-admin}"

# Собираем image с тегом tests
docker build -t tests .

# Запускаем контейнер под именем my_container из image tests
# В параметрах передаем маркер группы тестов


if [ $2 ]
then
  docker run --name my_container tests -m $2 --schema $SCHEMA --host $HOST --user $USER
else
  docker run --name my_container tests --schema $SCHEMA --host $HOST --user $USER
fi


# Копируем из контейнера созданный allure-report
docker cp my_container:/app/allure-results .

# Запускаем хост для отчета аллюр (утилита лежит локально)
$1 serve allure-results

# Удаляем из системы созданный контейнер и образ
docker system prune -f
docker image rm tests
