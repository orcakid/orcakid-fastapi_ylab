from fastapi import HTTPException, status
from sqlalchemy.orm import Session
# 1
from models import Dish, Menu, Submenu
from schemas import (
    BaseDish, CreateDish, CreateMenu, CreateSubmenu,
    PatchMenu, PatchSubmenu
)


def get_list_menu(db: Session):
    return db.query(Menu).all()

def get_menu(db: Session, menu_id: int):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )
    return menu


def count_submenu(db: Session, id):
    return db.query(Submenu).filter(Submenu.menu_id == id).all()

def create_menu_table(menu: CreateMenu, count_sub):
    new_menu = Menu(
        title=menu.title,
        description=menu.description,
        submenus_count=len(count_sub),
    )
    return new_menu

def chehing_exist(db: Session, id, new_menu: Menu):
    menu_db = db.query(Menu).filter(Menu.id==id).first()
    if menu_db is None:
        db.add(new_menu)
        db.commit()
        return new_menu
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='menu already exist',
        )

def create_menu(db: Session, menu: CreateMenu):
    count_sub = count_submenu(db,menu.id)
    new_menu = create_menu_table(menu=menu, count_sub=count_sub)
    check = chehing_exist(db=db,id=menu.id, new_menu=new_menu)
    return check
    
def update_menu(db: Session, menu_id: int, menu: PatchMenu):
    menu_to_update = get_menu(db=db, menu_id=menu_id)
    if menu_to_update:
        menu_to_update.id = menu_id
        menu_to_update.title = menu.title
        menu_to_update.description = menu.description
        db.commit()
        db.refresh(menu_to_update)
        return menu_to_update
    return menu_to_update


def delete_menu(db: Session, menu_id: int):
    menu_for_delete = get_menu(db=db, menu_id=menu_id)
    if menu_for_delete:
        db.delete(menu_for_delete)
        db.commit()
        return {'status': True, 'message': 'The menu has been deleted'}
    return menu_for_delete


def get_one_submenu_by_id(db: Session, menu_id: int, submenu_id: int):
    one_submenu = (
        db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
)
    if one_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )
    else:
        return one_submenu


def get_submenu_list(db: Session, menu_id: int):
    all_s_menu = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    return all_s_menu


def count_dish_for_submenu(db: Session, id_sub):
    return db.query(Dish).filter(Dish.submenu_id == id_sub).all()


def create_submenu_table(db: Session, menu_id: int, sub: CreateSubmenu):
    new_submenu = Submenu(
        title=sub.title,
        description=sub.description,
        menu_id=menu_id,
        #dishes_count=len(count_dish_for_submenu(db=db, id_sub=sub.id))
    )
    return new_submenu

def checking_submenu(db: Session, id, new_submenu):
    db_sub = db.query(Submenu).filter(Submenu.id == id).first()
    if db_sub is None:
            db.add(new_submenu)
            db.commit()
            return new_submenu
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='menu already exist',
        )
        
def create_submenu(db: Session, menu_id: int, sub: CreateSubmenu):
    new_submenu = create_submenu_table(db=db, menu_id=menu_id, sub=sub)
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu:
        submenu = checking_submenu(db=db,id=new_submenu.id, new_submenu=new_submenu)
    # учет количества сабменю в данном меню
        count_sub = count_submenu(db=db, id=menu_id)
        if count_sub is not None:
            d = db.query(Menu).filter(Menu.id == menu_id).first()
            d.submenus_count = len(count_sub)
            db.add(d)
            db.commit()
        return submenu


def update_submenu(db: Session, menu_id: int, submenu_id: int, submenu: PatchSubmenu):
    submenu_to_update = get_one_submenu_by_id(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if submenu_to_update is None:
        return submenu_to_update
    else:
        submenu_to_update.title = submenu.title
        submenu_to_update.description = submenu.description
        db.commit()
        db.refresh(submenu_to_update)
        return submenu_to_update
    
def count_dish_for_menu(db: Session, menu_id):
    return db.query(Dish).filter(Dish.menu_id == menu_id).all()
    
def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    s_menu_for_delete = get_one_submenu_by_id(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if s_menu_for_delete is None:
        return s_menu_for_delete
    else:
        count_sub = count_submenu(db=db,id=menu_id)
        menu = get_menu(db=db, menu_id=menu_id)
        menu.submenus_count = len(count_sub) - 1
        db.delete(s_menu_for_delete)
        db.commit()
        db.refresh(menu)
        count_dish_for_this_menu = count_dish_for_menu(db=db, menu_id=menu_id)
        menu.dishes_count = len(count_dish_for_this_menu)
        db.commit()
        db.refresh(menu)
        return {'status': True, 'message': 'The submenu has been deleted'}


def get_all_dishes(db: Session, menu_id: int, submenu_id: int):
    dish = (
        db.query(Dish)
        .filter(Dish.menu_id == menu_id)
        .filter(Dish.submenu_id == submenu_id)
        .all()
    )
    return dish if dish else []


def get_one_dishes(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    dish = (
        db.query(Dish)
        .join(Submenu, Submenu.id == Dish.submenu_id)
        .filter(
            Dish.id == dish_id,
            Submenu.id == submenu_id,
            Submenu.menu_id == menu_id,
        )
        .first()
    )
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )
    else:
        return dish
    
    
def create_dish_table(menu_id: int, submenu_id: int, dish: CreateDish):
    new_dish = Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
        menu_id=menu_id,
    )
    return new_dish

def checking_dish(db: Session, dish: CreateDish, new_dish):
    db_dish = db.query(Dish).filter(Dish.title == dish.title).first()
    if db_dish is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='dish already exist',
        )
    else:
        db.add(new_dish)
        db.commit()
        return new_dish
    
def create_dish(db: Session, menu_id: int, submenu_id: int, dish: CreateDish):
    new_dish = create_dish_table(menu_id=menu_id, submenu_id=submenu_id, dish=dish)
    menu = get_menu(db=db, menu_id=menu_id)
    submenu = get_one_submenu_by_id(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if menu is None or submenu is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='menu or submenu not exist',
        )
    db_dish = checking_dish(db=db, dish=new_dish, new_dish=new_dish)
    count_dish_submenu = count_dish_for_submenu(db=db, id_sub=submenu_id)
    count_dish_menu = count_dish_for_menu(db=db, menu_id=menu_id)
    
    menu.dishes_count = len(count_dish_menu)
    submenu.dishes_count = len(count_dish_submenu)
    db.add(menu)
    db.add(submenu)
    db.commit()
    db.refresh(menu)
    db.refresh(submenu)
    return db_dish

def update_dish(
    db: Session,
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: BaseDish,
):
    dish_for_update = get_one_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if dish_for_update is None:
        return dish_for_update
    else:
        dish_for_update.title = dish.title
        dish_for_update.description = dish.description
        dish_for_update.price = dish.price
        db.commit()
        db.refresh(dish_for_update)
        return dish_for_update
    
    
def delete_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    dish_for_delete = get_one_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if dish_for_delete is None:
        return dish_for_delete
    else:
        count_dish = get_all_dishes(db=db,menu_id=menu_id, submenu_id=submenu_id)
        
        menu_dish = get_menu(db=db, menu_id=menu_id)
        submenu_dish = get_one_submenu_by_id(db=db, menu_id=menu_id, submenu_id=submenu_id)
        menu_dish.dishes_count = len(count_dish) - 1
        submenu_dish.dishes_count = len(count_dish) - 1
        db.delete(dish_for_delete)
        db.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
