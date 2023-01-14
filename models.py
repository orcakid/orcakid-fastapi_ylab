from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


from database import BASE


class Menu(BASE):
    __tablename__ = 'menu'
    id = Column(Integer(),primary_key=True, index=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(String())
    submenus = relationship("Submenu", cascade="all, delete-orphan")
    dishes_count = Column(Integer, default=0)


class Submenu(BASE):
    __tablename__ = 'submenu'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    menus = relationship("Menu")
    #dishes_count = Column(Integer)







# class Dish(BASE):
#     __tablename__ = 'dish'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(200))
#     description = Column(String)
#     price = Column(Integer)
