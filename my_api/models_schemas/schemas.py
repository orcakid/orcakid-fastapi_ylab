from pydantic import BaseModel, Field


class BaseMenu(BaseModel):
    id: str | None = Field(default=0)
    title: str | None
    description: str | None
    dishes_count: int | None
    submenus_count: int | None

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
    id: str | None = Field(default=0)
    title: str | None
    description: str | None
    dishes_count: int | None

    class Config:
        orm_mode = True


class CreateSubmenu(BaseSubmenu):
    title: str | None
    description: str | None


class PatchSubmenu(BaseSubmenu):
    title: str | None
    description: str | None


class BaseDish(BaseModel):
    id: str | None = Field(default=0)
    title: str | None
    description: str | None
    price: str | None

    class Config:
        orm_mode = True


class CreateDish(BaseDish):
    title: str
    description: str
    price: str | None
