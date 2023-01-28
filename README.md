# Homework for ***Ylab***
_______
+ Склонируйте репозиторий: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
+ Создайте виртуальную среду: python -m venv venv
+ Активируйте ее: venv/Scripts/activate
+ Затем установите зависимости: pip install -r requirements.txt
+ Создайте в корневой директории файл ".env" для ваших переменных окружения: New-Item -Path . -Name ".env" -ItemType "file"
+ Заполните этот файл скопировав следущее:
   + #для контейнера с тестами
   
   + #DB_USER=postgres
   + #DB_PASSWORD=orca123
   + #DB_NAME=y_lab_fastapi_test
   + #DB_HOST=db_test
   + #DB_PORT=5432
   + #REDIS_HOST=redis

   + #для контейнера с приложением
   
   + #DB_USER=postgres
   + #DB_PASSWORD=orca123
   + #DB_NAME=y_lab_fastapi
   + #DB_HOST=db
   + #DB_PORT=5432
   + #REDIS_HOST=redis
______
#Запуск контейнера с приложением
+ Раскомментируйте в .env нужные переменные
+ Чтобы запустить контейнеры с приложением и бд используйте: docker-compose up -d
______
#Запуск контейнеров с тестами
+ Раскомментируйте в .env нужные переменные
+ Для контейнера с тестами используйте: docker-compose -f"docker-compose.test.yaml" up
_______
+ Clone me: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
+ Create your env: python -m venv venv
+ Activate this: venv/Scripts/activate
+ Then install requirements: pip install -r requirements.txt
+ Create file ".env" on this directory: New-Item -Path . -Name ".env" -ItemType "file"
+ Fill this file:
   + #for container with tests
   
   + #DB_USER=postgres
   + #DB_PASSWORD=orca123
   + #DB_NAME=y_lab_fastapi_test
   + #DB_HOST=db_test
   + #DB_PORT=5432
   + #REDIS_HOST=redis

   + #for container with app
   
   + #DB_USER=postgres
   + #DB_PASSWORD=orca123
   + #DB_NAME=y_lab_fastapi
   + #DB_HOST=db
   + #DB_PORT=5432
   + #REDIS_HOST=redis
_______
#Run container with app
+ Uncomment the required variables 
+ For container with app and db: docker-compose up -d
_______
#Run container with tests
+ Uncomment the required variables 
+ For container with tests: docker-compose -f"docker-compose.test.yaml" up
