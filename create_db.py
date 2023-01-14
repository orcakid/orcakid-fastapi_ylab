from database import BASE, engine
from models import Menu, Submenu, Dish


print('Creating database...')
BASE.metadata.create_all(engine)
