from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

import crud as crud
from database import get_db
from schemas import (
    BaseDish,
    BaseMenu,
    BaseSubmenu,
    CreateDish,
    CreateMenu,
    CreateSubmenu,
    PatchMenu,
    PatchSubmenu,
)

router = APIRouter()


@cache()
def get_cache():
    return 1


@router.get(
    "/api/v1/menus",
    response_model=List[BaseMenu],
    description="Возвращает список всех меню",
)
@cache(expire=60)
def get_menus(db: Session = Depends(get_db)):
    menu = crud.get_all_menus(db=db)
    return menu


@router.get(
    "/api/v1/menus/{menu_id}", response_model=BaseMenu, description="Поиск меню по id"
)
@cache(expire=60)
def get_one_menu(menu_id: int, db: Session = Depends(get_db)):
    return crud.get_menu(db=db, menu_id=menu_id)


@router.post(
    "/api/v1/menus",
    response_model=BaseMenu,
    status_code=status.HTTP_201_CREATED,
    description="Создает меню",
)
def create_menu(menu: CreateMenu, db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)


@router.patch(
    "/api/v1/menus/{menu_id}", response_model=BaseMenu, description="Обновляет меню"
)
def update_menu(menu_id: int, menu: PatchMenu, db: Session = Depends(get_db)):
    return crud.update_menu(db=db, menu=menu, menu_id=menu_id)


@router.delete("/api/v1/menus/{menu_id}", description="Удаляет меню")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    return crud.delete_menu(db=db, menu_id=menu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=List[BaseSubmenu],
    description="Возвращает список всех подменю определенного меню",
)
@cache(expire=60)
def get_list_submenu(menu_id: int, db: Session = Depends(get_db)):
    return crud.get_submenu_list(db=db, menu_id=menu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=BaseSubmenu,
    description="Подменю по id меню и подменню",
)
@cache(expire=60)
def get_one_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return crud.get_one_submenu_of_menu_by_id(
        db=db, menu_id=menu_id, submenu_id=submenu_id
    )


@router.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=BaseSubmenu,
    status_code=status.HTTP_201_CREATED,
    description="Создает подменю",
)
def create_submenu(menu_id: int, sub: CreateSubmenu, db: Session = Depends(get_db)):
    return crud.create_submenu(db=db, menu_id=menu_id, sub=sub)


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=BaseSubmenu,
    description="Обновляет подменю",
)
def update_submenu(
    menu_id: int, submenu_id: int, sub: PatchSubmenu, db: Session = Depends(get_db)
):
    return crud.update_submenu(
        db=db, submenu_id=submenu_id, menu_id=menu_id, submenu=sub
    )


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}", description="Удаляет подменю"
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return crud.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[BaseDish],
    description="Возвращает список всех блюд по id меню и подменю",
)
@cache(expire=60)
def get_dishes_list(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return crud.get_all_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=BaseDish,
    description="Возвращает блюдо по id",
)
@cache(expire=60)
def get_one_dishes(
    menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)
):
    return crud.get_one_dishes(
        db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
    )


@router.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=BaseDish,
    status_code=status.HTTP_201_CREATED,
    description="Создание блюда",
)
def create_dish(
    menu_id: int, submenu_id: int, dish: CreateDish, db: Session = Depends(get_db)
):
    return crud.create_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish=dish)


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=BaseDish,
    description="Обновляет блюдо",
)
def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: BaseDish,
    db: Session = Depends(get_db),
):
    return crud.update_dish(
        db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dish=dish
    )


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    description="удаляет блюдо",
)
def delete_dish(
    menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)
):
    return crud.delete_dish(
        db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
