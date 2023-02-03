from fastapi import FastAPI

from my_api.db.database import db_init
from my_api.routers.router import router

description = """
Приложение для создания меню, подмненю и блюд
с последующим внесение их в базу данных с
кэшированием запросов.
Приложение можно развернуть в докер-контейнерах
"""

app = FastAPI(
    title="Menu for Y_LAB",
    openapi_url="/my_api/openapi.json",
    description=description,
)


@app.on_event("startup")
async def on_startup():
    db_init


app.include_router(router=router)
