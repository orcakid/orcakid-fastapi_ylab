from models_and_schemas.models import Menu, Submenu, Dish
from db_api.database import BASE, engine


BASE.metadata.create_all(engine)