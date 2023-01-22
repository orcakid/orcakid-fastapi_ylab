from db_api.database import BASE, engine
from db_api.models import Menu, Submenu, Dish


print('Creating database...')
BASE.metadata.create_all(engine)
