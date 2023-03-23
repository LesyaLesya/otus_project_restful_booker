# Установка базового образа
FROM python:3.7

# Установка рабочей директории внутри контейнера и переход в нее
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Обновление pip и установка зависимостей
RUN pip install -U pip && pip install -r requirements.txt

# Копирование остальных файлов в /app
COPY . .

# Предустановка команды pytest и allure-отчет
ENTRYPOINT ["pytest", "--alluredir", "allure-results"]
