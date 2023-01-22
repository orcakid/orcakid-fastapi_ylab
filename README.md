# Homework for ***Ylab***
_______
1. Clone me: git clone https://github.com/orcakid/orcakid-fastapi_ylab.git .
2. Create your env: python -m venv venv
3. Activate this: venv/Scripts/activate
4. Then install requirements: pip install -r requirements.txt
5. Create file ".env" on this directory: New-Item -Path . -Name ".env" -ItemType "file"
6. Fill this file:
   1. DATABASE_URL=postgresql://postgres:orca123@db:5432/y_lab_fastapi
   2. DB_USER=postgres
   3. DB_PASSWORD=orca123
   4. DB_NAME=y_lab_fastapi
7. Run docker compose: docker-compose up -d
8. And run container with tests: docker-compose -f"docker-compose.test.yaml" up
