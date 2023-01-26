from fastapi import FastAPI
from models import Menu, Submenu, Dish
from database import db_init
from router import router


app = FastAPI()


@app.on_event("startup")
def on_startup():
    db_init()


app.include_router(router=router)


# from typing import List
# from fastapi import FastAPI, status, HTTPException
# from models import Menu, Submenu, Dish
# from database import Session_local, db_init
# from schemas import BaseMenu, BaseSubmenu, PatchMenu, BaseDish, PatchSubmenu, ResponseDish
# from dotenv import load_dotenv


# app = FastAPI()
# load_dotenv()


# db_local = Session_local()


# @app.on_event("startup")
# def on_startup():
#     db_init()

# @app.get('/api/v1/menus', response_model=List[BaseMenu], status_code=status.HTTP_200_OK)
# def get_menus():
#     menus = db_local.query(Menu).all()
#     if menus:
#         return menus
#     else:
#         return []


# @app.get('/api/v1/menus/{menu_id}', response_model=BaseMenu, status_code=status.HTTP_200_OK)
# def get_menu(menu_id: int):
#     menu = db_local.query(Menu).filter(Menu.id == menu_id).one_or_none()
#     if menu is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
#     return menu


# @app.post('/api/v1/menus', response_model=BaseMenu, status_code=status.HTTP_201_CREATED)
# def create_menu(menu: BaseMenu):
#     res = db_local.query(Submenu).filter(Submenu.menu_id == menu.id).all()
#     new_menu = Menu(
#         id=str(menu.id or 0),
#         title=menu.title,
#         description=menu.description,
#         submenus_count=len(res)
#         )
#     db_local.add(new_menu)
#     db_local.commit()
#     return new_menu


# @app.patch('/api/v1/menus/{menu_id}', response_model=PatchMenu, status_code=status.HTTP_200_OK)
# def update_menu(menu_id: int, menu: BaseMenu):
#     menu_to_update = db_local.query(Menu).filter(Menu.id == menu_id).one_or_none()
#     if menu_to_update is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
#     menu_to_update.id = menu_id
#     menu_to_update.title = menu.title
#     menu_to_update.description = menu.description
#     db_local.commit()
#     db_local.refresh(menu_to_update)
#     return menu_to_update


# @app.delete('/api/v1/menus/{menu_id}', status_code=status.HTTP_200_OK)
# def delete_menu(menu_id: int):
#     menu_for_delete = db_local.query(Menu).get(menu_id)
#     if menu_for_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     else:
#         db_local.delete(menu_for_delete)
#         db_local.commit()
#         return {
#             "status": True,
#             "message": "The menu has been deleted"
#         }


# @app.get('/api/v1/menus/{menu_id_for_submenu}/submenus', response_model=List[BaseSubmenu],
#         status_code=status.HTTP_200_OK)
# def get_submenu_of_menu_by_id(menu_id_for_submenu: int):
#     all_s_menu = db_local.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).all()
#     return all_s_menu


# @app.get('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu,
#         status_code=status.HTTP_200_OK)
# def get_one_submenu_of_menu_by_id(menu_id_for_submenu: int, submenu_id: int):
#     one_submenu = db_local.query(Submenu).filter(
#         Submenu.menu_id == menu_id_for_submenu).filter(
#         Submenu.id == submenu_id).one_or_none()

#     if one_submenu is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
#     else:
#         return one_submenu


# @app.post('/api/v1/menus/{menu_id_for_submenu}/submenus', response_model=BaseSubmenu,
#         status_code=status.HTTP_201_CREATED)
# def create_submenu(menu_id_for_submenu: int, sub: BaseSubmenu):
#     new_submenu = Submenu(
#         id=str(sub.id or 0),
#         title=sub.title,
#         description=sub.description,
#         menu_id=menu_id_for_submenu
#     )
#     menu = db_local.query(Menu).filter(Menu.id==menu_id_for_submenu).first()
#     if menu:
#         db_local.add(new_submenu)
#         db_local.commit()
#     res = db_local.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).all()
#     if res is not None:
#         d = db_local.query(Menu).filter(Menu.id == menu_id_for_submenu).first()
#         d.submenus_count = len(res)
#         db_local.add(d)
#         db_local.commit()
#     return new_submenu


# @app.patch('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu,
#         status_code=status.HTTP_200_OK)
# def update_submenu(menu_id_for_submenu: int, submenu_id: int, submenu: PatchSubmenu):
#     submenu_to_update = db_local.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).filter(
#                                 Submenu.id == submenu_id).one_or_none()
#     if submenu_to_update is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
#     else:
#         submenu_to_update.title = submenu.title
#         submenu_to_update.description = submenu.description
#         db_local.commit()
#         db_local.refresh(submenu_to_update)
#         return submenu_to_update


# @app.delete('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}')
# def delete_submenu(menu_id_for_submenu: int, submenu_id: int):
#     s_menu_for_delete = db_local.query(Submenu).filter(Submenu.id == submenu_id).first()
#     if s_menu_for_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     else:
#         res = db_local.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).all()
#         d = db_local.query(Menu).filter(Menu.id == menu_id_for_submenu).first()
#         d.submenus_count = len(res) - 1
#         db_local.delete(s_menu_for_delete)
#         db_local.commit()
#         db_local.refresh(d)
#         count_dish_for_this_menu = db_local.query(Dish).filter(Dish.menu_id == menu_id_for_submenu).all()
#         d.dishes_count = len(count_dish_for_this_menu)
#         db_local.commit()
#         db_local.refresh(d)
#         return {
#             "status": True,
#             "message": "The submenu has been deleted"
#             }


# @app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[BaseDish],
#         status_code=status.HTTP_200_OK)
# def get_all_dishes(menu_id: int, submenu_id: int):
#     dish = db_local.query(Dish).filter(Dish.menu_id==menu_id).filter(Dish.submenu_id==submenu_id).all()
#     return dish if dish else []


# @app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=BaseDish,
#         status_code=status.HTTP_200_OK)
# def get_one_dishes(menu_id: int, submenu_id: int, dish_id: int):
#     dish = db_local.query(Dish).join(Submenu, Submenu.id == Dish.submenu_id).filter(
#                                 Dish.id == dish_id,
#                                 Submenu.id == submenu_id,
#                                 Submenu.menu_id == menu_id).first()
#     if dish is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
#     else:
#         return dish


# @app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=ResponseDish,
#         status_code=status.HTTP_201_CREATED)
# def create_dish(menu_id: int, submenu_id: int, dish: BaseDish):
#     new_dish = Dish(
#         title=dish.title,
#         description=dish.description,
#         price=dish.price,
#         submenu_id=submenu_id,
#         menu_id=menu_id,
#         )
#     #блюдо
#     db_dish = db_local.query(Dish).filter(Dish.title == new_dish.title).first()
#     menu = db_local.query(Menu).filter(Menu.id == menu_id).first()
#     submenu = db_local.query(Submenu).filter(Submenu.id == submenu_id).first()
#     if db_dish is not None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='dish already exist')
#     elif menu is None or submenu is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='menu or submenu not exist'
#         )
#     else:
#         db_local.add(new_dish)
#         db_local.commit()
#         count_dish_submenu = db_local.query(Dish).filter(Dish.submenu_id == submenu_id).all()
#         count_dish_menu = db_local.query(Dish).filter(Dish.menu_id == menu_id).all()
#         menu_dish = db_local.query(Menu).filter(Menu.id == menu_id).first()
#         submenu_dish = db_local.query(Submenu).filter(Submenu.id == submenu_id).first()
#         menu_dish.dishes_count = len(count_dish_menu)
#         submenu_dish.dishes_count = len(count_dish_submenu)
#         db_local.add(menu_dish)
#         db_local.add(submenu_dish)
#         db_local.commit()
#         db_local.refresh(menu_dish)
#         db_local.refresh(submenu_dish)
#         return new_dish


# @app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
#         response_model=BaseDish,
#         status_code=status.HTTP_200_OK)
# def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: BaseDish):
#     dish_for_update = db_local.query(Dish).filter(Dish.id == dish_id).filter(
#         Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
#     if dish_for_update is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
#     else:
#         dish_for_update.title = dish.title
#         dish_for_update.description = dish.description
#         dish_for_update.price = dish.price
#         db_local.commit()
#         db_local.refresh(dish_for_update)
#         return dish_for_update


# @app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
#             status_code=status.HTTP_200_OK)
# def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
#     dish_for_delete = db_local.query(Dish).filter(Dish.id == dish_id).filter(
#         Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
#     if dish_for_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
#     else:
#         count_dish = db_local.query(Dish).filter(Dish.menu_id == menu_id).filter(
#         Dish.submenu_id == submenu_id).all()
#         menu_dish = db_local.query(Menu).filter(Menu.id == menu_id).first()
#         submenu_dish = db_local.query(Submenu).filter(Submenu.id == submenu_id).first()
#         menu_dish.dishes_count = len(count_dish) - 1
#         submenu_dish.dishes_count = len(count_dish) - 1
#         db_local.delete(dish_for_delete)
#         db_local.commit()
#         return {
#             "status": True,
#             "message": "The dish has been deleted"
#         }
