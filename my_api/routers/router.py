from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from my_api.cruds_op import cache_operations as cache
from my_api.cruds_op import db_crud as crud2
from my_api.db.database import get_db
from my_api.models_schemas import schemas

router = APIRouter()


@router.get(
    "/api/v1/menus",
    response_model=list[schemas.BaseMenu],
    description="Возвращает список всех меню",
    summary="Возвращает список всех меню",
    tags=["Menu"],
)
def get_menus(db: Session = Depends(get_db)):
    menu = crud2.get_list_menu(db=db)
    cache.cache_list_item(array=menu, type="list_menu")
    return menu


@router.get(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.BaseMenu,
    description="Поиск меню по id",
    summary="Поиск меню по id",
    tags=["Menu"],
)
def get_one_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = crud2.get_menu(db=db, menu_id=menu_id)
    cache.cache_item(id_item=menu_id, item=menu, type="menu")
    return menu


@router.post(
    "/api/v1/menus",
    response_model=schemas.BaseMenu,
    status_code=status.HTTP_201_CREATED,
    description="Создает меню",
    summary="Создает меню",
    tags=["Menu"],
)
def create_menu(menu: schemas.CreateMenu, db: Session = Depends(get_db)):
    return crud2.create_menu(db=db, menu=menu)


@router.patch(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.BaseMenu,
    description="Обновляет меню",
    summary="Обновляет меню",
    tags=["Menu"],
)
def update_menu(menu_id: int, menu: schemas.PatchMenu, db: Session = Depends(get_db)):
    return crud2.update_menu(db=db, menu=menu, menu_id=menu_id)


@router.delete(
    "/api/v1/menus/{menu_id}",
    description="Удаляет меню",
    tags=["Menu"],
    summary="Удаляет меню",
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    return crud2.delete_menu(db=db, menu_id=menu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=list[schemas.BaseSubmenu],
    description="Возвращает список всех подменю определенного меню",
    summary="Возвращает список всех подменю определенного меню",
    tags=["Subenu"],
)
def get_list_submenu(menu_id: int, db: Session = Depends(get_db)):
    submenu = crud2.get_submenu_list(db=db, menu_id=menu_id)
    cache.cache_list_item(array=submenu, type="list_submenu")
    return submenu


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.BaseSubmenu,
    description="Подменю по id меню и подменню",
    summary="Подменю по id меню и подменню",
    tags=["Subenu"],
)
def get_one_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = crud2.get_one_submenu_by_id(
        db=db,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    cache.cache_item(id_item=submenu_id, item=submenu, type="submenu")
    return submenu


@router.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=schemas.BaseSubmenu,
    status_code=status.HTTP_201_CREATED,
    description="Создает подменю",
    summary="Создает подменю",
    tags=["Subenu"],
)
def create_submenu_rout(
    menu_id: int,
    sub: schemas.BaseSubmenu,
    db: Session = Depends(get_db),
):
    return crud2.create_submenu(db=db, menu_id=menu_id, sub=sub)


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.BaseSubmenu,
    description="Обновляет подменю",
    summary="Обновляет подменю",
    tags=["Subenu"],
)
def update_submenu(
    menu_id: int,
    submenu_id: int,
    sub: schemas.PatchSubmenu,
    db: Session = Depends(get_db),
):
    return crud2.update_submenu(
        db=db,
        submenu_id=submenu_id,
        menu_id=menu_id,
        submenu=sub,
    )


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    description="Удаляет подменю",
    summary="Удаляет подменю",
    tags=["Subenu"],
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return crud2.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.BaseDish],
    description="Возвращает список всех блюд по id меню и подменю",
    summary="Возвращает список всех блюд по id меню и подменю",
    tags=["Dish"],
)
def get_dishes_list(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    dish = crud2.get_all_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id)
    cache.cache_list_item(array=dish, type="list_dish")
    return dish


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.BaseDish,
    description="Возвращает блюдо по id",
    summary="Возвращает блюдо по id",
    tags=["Dish"],
)
def get_one_dishes(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    db: Session = Depends(get_db),
):
    dish = crud2.get_one_dishes(
        db=db,
        dish_id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    cache.cache_item(item=dish, id_item=dish_id, type="dish")
    return dish


@router.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.BaseDish,
    status_code=status.HTTP_201_CREATED,
    description="Создание блюда",
    summary="Создание блюда",
    tags=["Dish"],
)
def create_dish(
    menu_id: int,
    submenu_id: int,
    dish: schemas.CreateDish,
    db: Session = Depends(get_db),
):
    return crud2.create_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish=dish)


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.BaseDish,
    description="Обновляет блюдо",
    summary="Обновляет блюдо",
    tags=["Dish"],
)
def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: schemas.BaseDish,
    db: Session = Depends(get_db),
):
    return crud2.update_dish(
        db=db,
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        dish=dish,
    )


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    description="удаляет блюдо",
    summary="удаляет блюдо",
    tags=["Dish"],
)
def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    db: Session = Depends(get_db),
):
    return crud2.delete_dish(
        db=db,
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
