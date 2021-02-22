#!/bin/bash

# Собираем image с тегом tests
docker build -t tests .


# Запускаем контейнер под именем my_container из image tests
# В параметрах передаем логин, пароль, количество потоков для запуска и маркер
docker run --name my_container tests --login $1 --passw $2 -n 2 -m all_tests

# Копируем из контейнера созданный allure-report
docker cp my_container:/app/allure-results .

# Запускаем хост для отчета аллюр (утилита лежит локально)
/Applications/allure/bin/allure serve allure-results

# Удаляем из системы созданный контейнер и образ
docker system prune -f
docker image rm tests
