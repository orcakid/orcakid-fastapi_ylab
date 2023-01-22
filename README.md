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
+ Теперь запустите первые два контейнера с приложением и базой данных: docker-compose up -d
+ И наконец запуск отдельного контейнера с тестами: docker-compose -f"docker-compose.test.yaml" up
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
+ Run docker compose: docker-compose up -d
+ And run container with tests: docker-compose -f"docker-compose.test.yaml" up
