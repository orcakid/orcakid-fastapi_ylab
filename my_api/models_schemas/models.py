from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from my_api.db.database import BASE


class Menu(BASE):
    __tablename__ = "menu"
    id = Column(Integer(), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String())
    submenus = relationship(
        "Submenu",
        back_populates="menus",
        cascade="all, delete-orphan",
    )
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)


class Submenu(BASE):
    __tablename__ = "submenu"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey("menu.id"))
    menus = relationship("Menu", back_populates="submenus")
    dishes_count = Column(Integer, default=0)
    dishes = relationship(
        "Dish",
        back_populates="submenus1",
        cascade="all, delete-orphan",
    )


class Dish(BASE):
    __tablename__ = "dish"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(String)
    price = Column(Float(round(2)))
    submenu_id = Column(Integer, ForeignKey("submenu.id"))
    menu_id = Column(Integer, ForeignKey("menu.id"))
    submenus1 = relationship("Submenu", back_populates="dishes")
