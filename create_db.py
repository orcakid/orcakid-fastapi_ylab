from models import Menu, Submenu, Dish
from database import BASE, engine


BASE.metadata.create_all(engine)