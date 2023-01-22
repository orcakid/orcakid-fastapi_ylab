from typing import List
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi import FastAPI, status, HTTPException
from models import Menu, Submenu, Dish
#from database import Session_local
import os
from schemas import BaseMenu, BaseSubmenu, PatchMenu, BaseDish, PatchSubmenu
from dotenv import load_dotenv

app = FastAPI()
load_dotenv(".env")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


#db = Session_local()



@app.get('/api/v1/menus', response_model=List[BaseMenu], status_code=status.HTTP_200_OK)
def get_menus():
    menus = db.session.query(Menu).all()
    if menus:
        return menus
    else:
        return []


@app.get('/api/v1/menus/{menu_id}', response_model=BaseMenu, status_code=status.HTTP_200_OK)
def get_menu(menu_id: int):
    menu = db.session.query(Menu).filter(Menu.id == menu_id).one_or_none()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return menu


@app.post('/api/v1/menus', response_model=BaseMenu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: BaseMenu):
    res = db.session.query(Submenu).filter(Submenu.menu_id == menu.id).all()
    new_menu = Menu(
        id=str(menu.id or 0),
        title=menu.title,
        description=menu.description,
        submenus_count=len(res)
        )
    db.session.add(new_menu)
    db.session.commit()
    return new_menu


@app.patch('/api/v1/menus/{menu_id}', response_model=PatchMenu, status_code=status.HTTP_200_OK)
def update_menu(menu_id: int, menu: BaseMenu):
    menu_to_update = db.session.query(Menu).filter(Menu.id == menu_id).one_or_none()
    if menu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    menu_to_update.id = menu_id
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description
    db.session.commit()
    db.session.refresh(menu_to_update)
    return menu_to_update


@app.delete('/api/v1/menus/{menu_id}', status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int):
    menu_for_delete = db.session.query(Menu).get(menu_id)
    if menu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.session.delete(menu_for_delete)
        db.session.commit()
        return {
            "status": True,
            "message": "The menu has been deleted"
        }


@app.get('/api/v1/menus/{menu_id_for_submenu}/submenus', response_model=List[BaseSubmenu],
        status_code=status.HTTP_200_OK)
def get_submenu_of_menu_by_id(menu_id_for_submenu: int):    
    all_s_menu = db.session.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).all()
    return all_s_menu


@app.get('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu,
        status_code=status.HTTP_200_OK)
def get_one_submenu_of_menu_by_id(menu_id_for_submenu: int, submenu_id: int):
    one_submenu = db.session.query(Submenu).filter(
        Submenu.menu_id == menu_id_for_submenu).filter(
        Submenu.id == submenu_id).one_or_none()
 
    if one_submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    else:
        return one_submenu


@app.post('/api/v1/menus/{menu_id_for_submenu}/submenus', response_model=BaseSubmenu,
        status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id_for_submenu: int, sub: BaseSubmenu):
    new_submenu = Submenu(
        id=str(sub.id or 0),
        title=sub.title,
        description=sub.description,
        menu_id=menu_id_for_submenu
    )
    db.session.add(new_submenu)
    db.session.commit()
    res = db.session.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).all()
    if res is not None:
        d = db.session.query(Menu).filter(Menu.id == menu_id_for_submenu).first()
        d.submenus_count = len(res)
        db.session.add(d)
        db.session.commit()
    return new_submenu


@app.patch('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu,
        status_code=status.HTTP_200_OK)
def update_submenu(menu_id_for_submenu: int, submenu_id: int, submenu: PatchSubmenu):
    submenu_to_update = db.session.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).filter(
                                Submenu.id == submenu_id).one_or_none()
    if submenu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    else:
        submenu_to_update.title = submenu.title
        submenu_to_update.description = submenu.description
        db.session.commit()
        db.session.refresh(submenu_to_update)
        return submenu_to_update


@app.delete('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}')
def delete_submenu(menu_id_for_submenu: int, submenu_id: int):
    s_menu_for_delete = db.session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if s_menu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        res = db.session.query(Submenu).filter(Submenu.menu_id == menu_id_for_submenu).all()
        d = db.session.query(Menu).filter(Menu.id == menu_id_for_submenu).first()
        d.submenus_count = len(res) - 1
        db.session.delete(s_menu_for_delete)
        db.session.commit()
        db.session.refresh(d)
        count_dish_for_this_menu = db.session.query(Dish).filter(Dish.menu_id == menu_id_for_submenu).all()
        d.dishes_count = len(count_dish_for_this_menu)
        db.session.commit()
        db.session.refresh(d)
        return {
            "status": True,
            "message": "The submenu has been deleted"
            }


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[BaseDish],
        status_code=status.HTTP_200_OK)
def get_all_dishes(menu_id: int, submenu_id: int):
    dish = db.session.query(Dish).filter(Dish.menu_id==menu_id).filter(Dish.submenu_id==submenu_id).all()
    return dish if dish else []


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=BaseDish,
        status_code=status.HTTP_200_OK)
def get_one_dishes(menu_id: int, submenu_id: int, dish_id: int):
    dish = db.session.query(Dish).join(Submenu, Submenu.id == Dish.submenu_id).filter(
                                Dish.id == dish_id,
                                Submenu.id == submenu_id,
                                Submenu.menu_id == menu_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    else:
        return dish


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=BaseDish,
        status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: int, submenu_id: int, dish: BaseDish):
    new_dish = Dish(
        id=str(dish.id or 0),
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
        menu_id=menu_id,
        )
    
    #блюдо
    db_dish = db.session.query(Dish).filter(Dish.title == new_dish.title).first()
    menu = db.session.query(Menu).filter(Menu.id == menu_id).first()
    submenu = db.session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if db_dish is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='dish already exist')
    elif menu is None or submenu is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='menu or submenu not exist'
        )
    else:
        db.session.add(new_dish)
        db.session.commit()
        count_dish_submenu = db.session.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        count_dish_menu = db.session.query(Dish).filter(Dish.menu_id == menu_id).all()
        menu_dish = db.session.query(Menu).filter(Menu.id == menu_id).first()
        submenu_dish = db.session.query(Submenu).filter(Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish_menu)
        submenu_dish.dishes_count = len(count_dish_submenu)
        db.session.add(menu_dish)
        db.session.add(submenu_dish)
        db.session.commit()
        db.session.refresh(menu_dish)
        db.session.refresh(submenu_dish)
        return new_dish


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        response_model=BaseDish,
        status_code=status.HTTP_200_OK)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: BaseDish):
    dish_for_update = db.session.query(Dish).filter(Dish.id == dish_id).filter(
        Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
    if dish_for_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        dish_for_update.title = dish.title
        dish_for_update.description = dish.description
        dish_for_update.price = dish.price
        db.session.commit()
        db.session.refresh(dish_for_update)
        return dish_for_update


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            status_code=status.HTTP_200_OK)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
    dish_for_delete = db.session.query(Dish).filter(Dish.id == dish_id).filter(
        Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
    if dish_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        count_dish = db.session.query(Dish).filter(Dish.menu_id == menu_id).filter(
        Dish.submenu_id == submenu_id).all()
        menu_dish = db.session.query(Menu).filter(Menu.id == menu_id).first()
        submenu_dish = db.session.query(Submenu).filter(Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish) - 1
        submenu_dish.dishes_count = len(count_dish) - 1
        db.session.delete(dish_for_delete)
        db.session.commit()
        return {
            "status": True,
            "message": "The dish has been deleted"
        }
