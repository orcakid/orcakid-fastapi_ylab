from fastapi import APIRouter, Depends, status

from my_api.models_schemas import schemas

from ..service.operations import DishCrud, MenuCrud, SubmenuCrud

router = APIRouter()


@router.get(
    "/api/v1/menus",
    response_model=list[schemas.BaseMenu],
    description="Возвращает список всех меню",
    summary="Возвращает список всех меню",
    tags=["Menu"],
)
def get_menus(service: MenuCrud = Depends()):
    return service.get_list_menu()


@router.get(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.BaseMenu,
    description="Поиск меню по id",
    summary="Поиск меню по id",
    tags=["Menu"],
)
def get_one_menu(menu_id: int, service: MenuCrud = Depends()):
    return service.get_one_menu(menu_id=menu_id)


@router.post(
    "/api/v1/menus",
    response_model=schemas.BaseMenu,
    status_code=status.HTTP_201_CREATED,
    description="Создает меню",
    summary="Создает меню",
    tags=["Menu"],
)
def create_menu(menu: schemas.CreateMenu, service: MenuCrud = Depends()):
    return service.create_menu(menu=menu)


@router.patch(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.BaseMenu,
    description="Обновляет меню",
    summary="Обновляет меню",
    tags=["Menu"],
)
def update_menu(menu_id: int, menu: schemas.CreateMenu, service: MenuCrud = Depends()):
    return service.update_menu(menu_id=menu_id, menu=menu)


@router.delete(
    "/api/v1/menus/{menu_id}",
    description="Удаляет меню",
    tags=["Menu"],
    summary="Удаляет меню",
)
def delete_menu(menu_id: int, service: MenuCrud = Depends()):
    return service.delete_menu(menu_id=menu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=list[schemas.BaseSubmenu],
    description="Возвращает список всех подменю определенного меню",
    summary="Возвращает список всех подменю определенного меню",
    tags=["Subenu"],
)
def get_list_submenu(menu_id: int, service: SubmenuCrud = Depends()):
    return service.get_submenu_list(menu_id=menu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.BaseSubmenu,
    description="Подменю по id меню и подменню",
    summary="Подменю по id меню и подменню",
    tags=["Subenu"],
)
def get_one_submenu(menu_id: int, submenu_id: int, service: SubmenuCrud = Depends()):
    return service.get_one_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)


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
    sub: schemas.CreateSubmenu,
    service: SubmenuCrud = Depends(),
):
    return service.create_submenu(menu_id=menu_id, sub=sub)


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
    sub: schemas.CreateSubmenu,
    service: SubmenuCrud = Depends(),
):
    return service.update_submenu(menu_id=menu_id, submenu=sub, submenu_id=submenu_id)


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    description="Удаляет подменю",
    summary="Удаляет подменю",
    tags=["Subenu"],
)
def delete_submenu(menu_id: int, submenu_id: int, service: SubmenuCrud = Depends()):
    return service.delete_submenu(submenu_id=submenu_id, menu_id=menu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.BaseDish],
    description="Возвращает список всех блюд по id меню и подменю",
    summary="Возвращает список всех блюд по id меню и подменю",
    tags=["Dish"],
)
def get_dishes_list(menu_id: int, submenu_id: int, service: DishCrud = Depends()):
    return service.get_all_dishes(menu_id=menu_id, submenu_id=submenu_id)


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
    service: DishCrud = Depends(),
):
    return service.get_one_dishes(
        submenu_id=submenu_id,
        dish_id=dish_id,
        menu_id=menu_id,
    )


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
    service: DishCrud = Depends(),
):
    return service.create_dish(menu_id=menu_id, dish=dish, submenu_id=submenu_id)


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
    dish: schemas.CreateDish,
    service: DishCrud = Depends(),
):
    return service.update_dish(
        submenu_id=submenu_id,
        menu_id=menu_id,
        dish=dish,
        dish_id=dish_id,
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
    service: DishCrud = Depends(),
):
    return service.delete_dish(submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id)
