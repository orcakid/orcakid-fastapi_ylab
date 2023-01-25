from models import Menu, Submenu, Dish
from database import BASE, engine_test


BASE.metadata.create_all(engine_test)