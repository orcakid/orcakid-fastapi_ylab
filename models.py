from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


from database import BASE


class Menu(BASE):
    __tablename__ = 'menu'
    id = Column(Integer(),primary_key=True, index=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(String())
    submenus = relationship("Submenu", cascade="all, delete-orphan")
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)


class Submenu(BASE):
    __tablename__ = 'submenu'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    menus = relationship("Menu")
    dishes_count = Column(Integer, default=0)
    dish = relationship("Dish", cascade="all, delete-orphan")


class Dish(BASE):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    # как сделать, чтобы одно и тоже блюдо не могло быть в разных подменю?
    title = Column(String(200), unique=True)
    description = Column(String)
    price = Column(Float(round(2)))

    submenu_id = Column(Integer, ForeignKey('submenu.id'))
    menu_id = Column(Integer, ForeignKey('menu.id'))
    submenu = relationship('Submenu')
