from pydantic import BaseModel
from typing import Optional


# используется для сериализации или изменения обьектов, так как идет валидация типов
class BaseMenu(BaseModel):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    dishes_count: Optional[int]
    class Config:
        #автоматически сирелизует обьекты склалхими в джейсон
        orm_mode=True

class PatchMenu(BaseMenu):
    id: Optional[int]
    title: str
    description: str
    dishes_count: Optional[int]

class MenuUpdate(BaseMenu):
    dishes_count: int


class BaseSubmenu(BaseModel):
    id: Optional[int]
    title: str
    description: str

    class Config:
        orm_mode=True



#
# class Dish(BaseModel):
#     id: int
#     title: str
#     description: str
#     price: int
#
#     class Config:
#         orm_mode=True
