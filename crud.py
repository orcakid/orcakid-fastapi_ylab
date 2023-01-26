from models import Menu, Submenu, Dish
from sqlalchemy.orm import Session
from schemas import BaseMenu, BaseSubmenu, PatchMenu, BaseDish, PatchSubmenu, CreateDish, CreateMenu, CreateSubmenu
from fastapi import status, HTTPException


def get_all_menus(db: Session):
    return db.query(Menu).all()


def get_menu(db: Session, menu_id: int):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return menu


def create_menu(db: Session, menu: CreateMenu):
    #количесвто подменю
    res = db.query(Submenu).filter(Submenu.menu_id == menu.id).all()
    new_menu = Menu(
        title=menu.title,
        description=menu.description,
        submenus_count=len(res)
        )
    menu_db = db.query(Menu).filter(Menu.id == menu.id).first()
    if menu_db is None:
        db.add(new_menu)
        db.commit()
        return new_menu
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='menu already exist')


def update_menu(db: Session, menu_id: int, menu: PatchMenu):
    menu_to_update = db.query(Menu).filter(Menu.id == menu_id).one_or_none()
    if menu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    menu_to_update.id = menu_id
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description
    db.commit()
    db.refresh(menu_to_update)
    return menu_to_update


def delete_menu(db: Session, menu_id: int):
    menu_for_delete = db.query(Menu).get(menu_id)
    if menu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.delete(menu_for_delete)
        db.commit()
        return {
            "status": True,
            "message": "The menu has been deleted"
        }


def get_submenu_list(db: Session, menu_id: int):    
    all_s_menu = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    return all_s_menu


def get_one_submenu_of_menu_by_id(db: Session, menu_id: int, submenu_id: int):
    one_submenu = db.query(Submenu).filter(
        Submenu.menu_id == menu_id).filter(
        Submenu.id == submenu_id).first()
    if one_submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    else:
        return one_submenu



def create_submenu(db: Session, menu_id: int, sub: CreateSubmenu):
    new_submenu = Submenu(
        title=sub.title,
        description=sub.description,
        menu_id=menu_id
    )
    menu = db.query(Menu).filter(Menu.id==menu_id).first()
    if menu:
        submenu = db.query(Submenu).filter(Submenu.id==sub.id).first()
        if submenu is None:
            db.add(new_submenu)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='menu already exist')
    #учет количества сабменю в данном меню
    res = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    if res is not None:
        d = db.query(Menu).filter(Menu.id == menu_id).first()
        d.submenus_count = len(res)
        db.add(d)
        db.commit()
    return new_submenu


def update_submenu(db: Session, menu_id: int, submenu_id: int, submenu: PatchSubmenu):
    submenu_to_update = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(
                                Submenu.id == submenu_id).first()
    if submenu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    else:
        submenu_to_update.title = submenu.title
        submenu_to_update.description = submenu.description
        db.commit()
        db.refresh(submenu_to_update)
        return submenu_to_update


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    s_menu_for_delete = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if s_menu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        res = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        menu.submenus_count = len(res) - 1
        db.delete(s_menu_for_delete)
        db.commit()
        db.refresh(menu)
        count_dish_for_this_menu = db.query(Dish).filter(Dish.menu_id == menu_id).all()
        menu.dishes_count = len(count_dish_for_this_menu)
        db.commit()
        db.refresh(menu)
        return {
            "status": True,
            "message": "The submenu has been deleted"
            }


def get_all_dishes(db: Session, menu_id: int, submenu_id: int):
    dish = db.query(Dish).filter(Dish.menu_id==menu_id).filter(Dish.submenu_id==submenu_id).all()
    return dish if dish else []


def get_one_dishes(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    dish = db.query(Dish).join(Submenu, Submenu.id == Dish.submenu_id).filter(
                                Dish.id == dish_id,
                                Submenu.id == submenu_id,
                                Submenu.menu_id == menu_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    else:
        return dish


def create_dish(db: Session, menu_id: int, submenu_id: int, dish: CreateDish):
    new_dish = Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
        menu_id=menu_id,
        )
    #блюдо
    db_dish = db.query(Dish).filter(Dish.title == new_dish.title).first()
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if db_dish is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='dish already exist')
    elif menu is None or submenu is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='menu or submenu not exist'
        )
    else:
        db.add(new_dish)
        db.commit()
        count_dish_submenu = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        count_dish_menu = db.query(Dish).filter(Dish.menu_id == menu_id).all()
        menu_dish = db.query(Menu).filter(Menu.id == menu_id).first()
        submenu_dish = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish_menu)
        submenu_dish.dishes_count = len(count_dish_submenu)
        db.add(menu_dish)
        db.add(submenu_dish)
        db.commit()
        db.refresh(menu_dish)
        db.refresh(submenu_dish)
        return new_dish


def update_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int, dish: BaseDish):
    dish_for_update = db.query(Dish).filter(Dish.id == dish_id).filter(
        Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
    if dish_for_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        dish_for_update.title = dish.title
        dish_for_update.description = dish.description
        dish_for_update.price = dish.price
        db.commit()
        db.refresh(dish_for_update)
        return dish_for_update


def delete_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    dish_for_delete = db.query(Dish).filter(Dish.id == dish_id).filter(
        Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
    if dish_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        count_dish = db.query(Dish).filter(Dish.menu_id == menu_id).filter(
        Dish.submenu_id == submenu_id).all()
        menu_dish = db.query(Menu).filter(Menu.id == menu_id).first()
        submenu_dish = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish) - 1
        submenu_dish.dishes_count = len(count_dish) - 1
        db.delete(dish_for_delete)
        db.commit()
        return {
            "status": True,
            "message": "The dish has been deleted"
        }