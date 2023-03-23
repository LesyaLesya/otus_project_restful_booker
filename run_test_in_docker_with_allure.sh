#!/bin/bash

# Собираем image с тегом tests
docker build -t tests .


# Запускаем контейнер под именем my_container из image tests
# В параметрах передаем маркер группы тестов
if [ $2 ]
then
  docker run --name my_container tests -m $2
else
  docker run --name my_container tests
fi


# Копируем из контейнера созданный allure-report
docker cp my_container:/app/allure-results .

# Запускаем хост для отчета аллюр (утилита лежит локально)
$1 serve allure-results

# Удаляем из системы созданный контейнер и образ
docker system prune -f
docker image rm tests
