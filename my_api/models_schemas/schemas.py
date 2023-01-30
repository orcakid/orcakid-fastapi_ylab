from pydantic import BaseModel, Field


class BaseMenu(BaseModel):
    id: str | None = Field(default=0)
    title: str | None
    description: str | None
    dishes_count: int | None
    submenus_count: int | None

    class Config:
        orm_mode = True


class CreateMenu(BaseModel):
    title: str
    description: str


class BaseSubmenu(BaseModel):
    id: str | None = Field(default=0)
    title: str | None
    description: str | None
    dishes_count: int | None

    class Config:
        orm_mode = True


class CreateSubmenu(BaseModel):
    title: str | None
    description: str | None

    class Config:
        orm_mode = True


class BaseDish(BaseModel):
    id: str | None = Field(default=0)
    title: str | None
    description: str | None
    price: str | None

    class Config:
        orm_mode = True


class CreateDish(BaseModel):
    title: str
    description: str
    price: str | None
