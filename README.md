# Меню для ресторана
_______
+ Склонируйте репозиторий: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
+ Создайте виртуальную среду: python -m venv venv
+ Активируйте ее: venv/Scripts/activate
+ Затем установите зависимости: pip install -r requirements.txt
+ Создайте в корневой директории файл ".env" для ваших переменных окружения
+ Заполните этот файл скопировав следущее:
   + DB_USER=postgres
   + DB_PASSWORD=orca123
   + DB_NAME=y_lab_fastapi
   + DB_HOST=db
   + DB_PORT=5432
   + REDIS_HOST=redis
______
#Проверка линтеров
+ pre-commit run --all-files
______
#Запуск контейнера с приложением
+ Чтобы запустить контейнеры с приложением и бд используйте: docker-compose up -d
+ Документация опенапи: http://127.0.0.1:8000/my_api/openapi.json
______
#Запуск контейнеров с тестами
+ Для контейнера с тестами используйте: docker-compose -f"docker-compose.test.yaml" up
_______
+ Clone me: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
+ Create your env: python -m venv venv
+ Activate this: venv/Scripts/activate
+ Then install requirements: pip install -r requirements.txt
+ Create file ".env" on this directory
+ Fill this file:
   + DB_USER=postgres
   + DB_PASSWORD=orca123
   + DB_NAME=y_lab_fastapi
   + DB_HOST=db
   + DB_PORT=5432
   + REDIS_HOST=redis
______
#Сhecking linters
+ pre-commit run --all-files
_______
#Run container with app
+ For container with app and db: docker-compose up -d
+ documentation openapi: http://127.0.0.1:8000/my_api/openapi.json
_______
#Run container with tests
+ For container with tests: docker-compose -f"docker-compose.test.yaml" up
