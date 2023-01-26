from typing import Optional

from pydantic import BaseModel


class BaseMenu(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    dishes_count: Optional[int]
    submenus_count: Optional[int]

    # автоматически сирелизует обьекты склалхими в джейсон
    class Config:
        orm_mode = True


class CreateMenu(BaseMenu):
    title: str
    description: str


class PatchMenu(BaseMenu):
    title: str
    description: str


class BaseSubmenu(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True


class CreateSubmenu(BaseSubmenu):
    title: Optional[str]
    description: Optional[str]


class PatchSubmenu(BaseSubmenu):
    title: Optional[str]
    description: Optional[str]


class BaseDish(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    price: Optional[str]

    class Config:
        orm_mode = True


class CreateDish(BaseDish):
    title: str
    description: str
    price: str | None
