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
____

## Список необходимых предустановленных приложений и утилит

- Python3 - для запуска через консоль/ide
- Docker - для запуска тестов в контейнере и для Jenkins
- Allure - для получения отчета при запуске через консоль/ide/docker
- Jenkins - для запуска в Jenkins
____

## Установка проекта

- Скачать репозиторий на свою машину:

```
git clone https://github.com/LesyaLesya/otus_project_restful_booker.git
```

- Перейти в директорию скачанного репозитория

- Установить и активировать виртуальное окружение (для запуска тестов через консоль/ide)

```
python3 -m venv venv
source venv/bin/activate
```
- Обновить PIP и установить зависимости (для запуска тестов через консоль/ide)

```
pip install -U pip
pip install -r requirements.txt
```

- Выбрать интерпретатор для проекта (для запуска тестов через консоль/ide)
____

## Запуск тестов

### __В IDE PyCharm__

#### Запустить тесты в PyCharm 

В Terminal выполнить команду:

```
pytest -n 2 -m marker tests/
```
где:

- -n - во сколько потоков запускать тесты, если не указывать параметр при запуске - тесты будут запущены в 1 поток.
- -m - маркер, какую группу тестов запускать.
Варианты: create_booking, delete_booking, get_booking, get_booking_ids, patch_booking, put_booking
если не добавлять маркер - запускаются все тесты

#### Получить отчет Allure 

- В Terminal выполнить команду, в качестве параметра указав путь до исполняемого файла allure на вашей машине:

```
./run_allure_report.sh /path/to/allure/bin
Пример: ./run_allure_report.sh /Applications/allure/bin/allure
```

### __В Docker__

- Запустить Docker

- Запустить тесты и получить отчет командой в Terminal, в качестве параметров указав путь до исполняемого файла allure на вашей машине и маркер (опционально):

```
./run_test_in_docker_with_allure.sh  /path/to/allure/bin marker

Пример: ./run_test_in_docker_with_allure.sh /Applications/allure/bin/allure get_booking
Пример: ./run_test_in_docker_with_allure.sh /Applications/allure/bin/allure 

```

### __В Jenkins__

- Запустить Docker и Jenkins

- В Jenkins создать PipeLine

- Добавить в сборку параметры:
  + NODES - значение по-умолчанию 1
  + MARKER с вариантами на выбор 
  + DOCKER_PATH - путь до исполняемого файла Docker на машине
  
- Выбрать Pipeline script from SCM

- Выбрать SCM - Git

- Указать ссылку на репозиторий на Github

- Проверить название ветки - */main

- Сохранить пайплайн

- Собрать с необходимыми параметрами
____
