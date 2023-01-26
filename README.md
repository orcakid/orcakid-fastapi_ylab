# Homework for ***Ylab***
_______
+ Склонируйте репозиторий: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
+ Создайте виртуальную среду: python -m venv venv
+ Активируйте ее: venv/Scripts/activate
+ Затем установите зависимости: pip install -r requirements.txt
+ Создайте в корневой директории файл ".env" для ваших переменных окружения: New-Item -Path . -Name ".env" -ItemType "file"
+ Заполните этот файл скопировав следущее:
   + DATABASE_URL=postgresql://postgres:orca123@db:5432/y_lab_fastapi
   + DB_USER=postgres
   + DB_PASSWORD=orca123
   + DB_NAME=y_lab_fastapi
______
+ Чтобы запустить контейнеры с приложением и бд используйте: docker-compose up -d
______
+ Для контейнера с тестами используйте: docker-compose -f"docker-compose.test.yaml" up
_______
+ Clone me: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
+ Create your env: python -m venv venv
+ Activate this: venv/Scripts/activate
+ Then install requirements: pip install -r requirements.txt
+ Create file ".env" on this directory: New-Item -Path . -Name ".env" -ItemType "file"
+ Fill this file:
   + DATABASE_URL=postgresql://postgres:orca123@db:5432/y_lab_fastapi
   + DB_USER=postgres
   + DB_PASSWORD=orca123
   + DB_NAME=y_lab_fastapi
_______
+ For container with app and db: docker-compose up -d
_______
+ For container with tests: docker-compose -f"docker-compose.test.yaml" up
