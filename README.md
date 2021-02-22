## Описание проекта

Проект по автоматизации тестирования API ресурса restful-booker на курсе "Python QA Engineer " от OTUS.

Restful-booker - открытое API для тренировки работы с запросами.

[Ссылка на документацию API restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) 

+ В директории tests/ находятся файлы с тестами на методы API. Каждый файл - на отдельный метод.
  
  - tests/test_create_booking.py - CreateBooking
  - tests/test_delete_booking.py - DeleteBooking
  - tests/test_get_booking.py - GetBooking
  - tests/test_get_booking_ids.py - GetBookingIds
  - tests/test_partial_update_booking.py - PartialUpdateBooking
  - tests/test_update_booking.py - UpdateBooking

+ В файле conftest описан базовый класс создания ApiClient с методами GET, POST, PUT, PATCH, DELETE.
Создание экземпляра класса завернуто в фикстуру с областью видимости session (чтобы все тесты проходили с одним экземпляром класса в одной сессии), которая передается в тесты.
____

## Список необходимых предустановленных приложений и утилит

- Python3
- PyCharm
- Docker
- Allure
- Jenkins
____

## Установка проекта

- Скачать репозиторий на свою машину:

```
git clone https://github.com/LesyaLesya/otus_project_restful_booker.git
```

- Перейти в директорию скачанного репозитория

- Установить и активировать виртуальное окружение

```
python3 -m venv venv
source venv/bin/activate
```
- Обновить PIP и установить зависимости

```
pip install -U pip
pip install -r requirements.txt
```

- Выбрать интерпретатор для проекта
____

## Запуск тестов

### __В IDE PyCharm__

#### Запустить тесты в PyCharm 

В Terminal выполнить команду:

```
pytest -n 2 -m all_tests tests/ --login=admin --passw=password123
```
где:

- -n - во сколько потоков запускать тесты, если не указывать параметр при запуске - тесты будут запущены в 1 поток.

- -m - маркер, какие тесты запускать.
Варианты: all_tests, positive, negative.
  + all_tests - запускаются все тесты
  + postive - запускаются позитивные тесты
  + negative - запускаются негативные тесты
  
- --login - логин, необходимый для получения auth token, который используется в запросах PUT, PATCH, DELETE. Значение по-умолчанию admin (запускать с ним).

- --passw - пароль, необходимый для получения auth token, который используется в запросах PUT, PATCH, DELETE. Значение по-умолчанию password123 (запускать с ним).


#### Получить отчет Allure 

- В файле run_allure_report.sh указать путь до исполняемого файла allure на вашей машине.

- В Terminal выполнить команду:

```
./run_docker_allure.sh 
```

### __В Docker__

- Запустить Docker

- В файле run_docker_allure.sh указать путь до исполняемого файла allure на вашей машине.

- В файле run_docker_allure.sh по желанию изменить параметры запуска, например количество потоков или маркер.

- Запустить тесты и получить отчет командой в Terminal:

```
./run_docker_allure.sh 
```

### __В Jenkins__

- Запустить Docker и Jenkins

- Зайти в свой Jenkins

- Создать PipeLine

- Добавить в сборку параметры:
  + LOGIN - значение по-умолчанию admin
  + PASSW - значение по-умолчанию password123
  + NODES - значение по-умолчанию 1
  + MARKER с вариантами на выбор all_tests, positive, negative
  
- Выбрать Pipeline script from SCM

- Выбрать SCM - Git

- Указать ссылку на репозиторий на Github

- Проверить название ветки - */main

- Сохранить пайплайн

- Собрать с необходимыми параметрами
____