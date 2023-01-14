from typing import List
from fastapi import FastAPI, status, HTTPException

import models
from database import Session_local
from schemas import BaseMenu, BaseSubmenu, PatchMenu, Dish, UpgradeDish, PatchSubmenu

app = FastAPI()

# экземпляр сессии
db = Session_local()


# для сериализации меню по нашей схеме
@app.get('/api/v1/menus', response_model=List[BaseMenu], status_code=status.HTTP_200_OK)
def get_menus():
    menus = db.query(models.Menu).all()
    return menus


@app.get('/api/v1/menus/{menu_id}', response_model=BaseMenu, status_code=status.HTTP_200_OK)
def get_menu(menu_id: int):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).one_or_none()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return menu


@app.post('/api/v1/menus', response_model=BaseMenu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: BaseMenu):
    res = db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
    new_menu = models.Menu(
        # решает проблему сравнивания int в pk модели и id(str) на сервере
        id=str(menu.id or 0),
        title=menu.title,
        description=menu.description,
        dishes_count=len(res)
    )

    db.add(new_menu)
    db.commit()

    return new_menu


@app.patch('/api/v1/menus/{menu_id}', response_model=PatchMenu, status_code=status.HTTP_200_OK)
def update_menu(menu_id: int, menu: BaseMenu):
    menu_to_update = db.query(models.Menu).filter(models.Menu.id == menu_id).one_or_none()
    if menu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    menu_to_update.id = menu_id
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description

    db.commit()
    db.refresh(menu_to_update)
    return menu_to_update


@app.delete('/api/v1/menus/{menu_id}', response_model=BaseMenu, status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int):
    # При удалении меню удаляются вместе с его отношениями
    menu_for_delete = db.query(models.Menu).get(menu_id)
    if menu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.delete(menu_for_delete)
        db.commit()

    return menu_for_delete


###submenu###

@app.get('/api/v1/menus/{menu_id_for_submenu}/submenus', response_model=List[BaseSubmenu], status_code=status.HTTP_200_OK)
def get_submenu_of_menu_by_id(menu_id_for_submenu: int):
    all_s_menu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id_for_submenu).all()
    return all_s_menu


@app.get('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu, status_code=status.HTTP_200_OK)
def get_one_submenu_of_menu_by_id(menu_id_for_submenu: int, submenu_id: int):
    one_submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id_for_submenu).filter(
        models.Submenu.id == submenu_id).one_or_none()
    if one_submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    else:
        return one_submenu


@app.post('/api/v1/menus/{menu_id_for_submenu}/submenus', response_model=BaseSubmenu, status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id_for_submenu: int, sub: BaseSubmenu):
    new_submenu = models.Submenu(
        id=str(sub.id or 0),
        title=sub.title,
        description=sub.description,
        menu_id=menu_id_for_submenu
    )
    db.add(new_submenu)
    db.commit()

    res = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id_for_submenu).all()
    if res is None:
        pass
    else:
        d = db.query(models.Menu).filter(models.Menu.id==menu_id_for_submenu).first()
        d.submenus_count = len(res)
        db.add(d)
        db.commit()
    return new_submenu


@app.patch('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu, status_code=status.HTTP_200_OK)
def update_submenu(menu_id_for_submenu: int, submenu_id: int, submen: PatchSubmenu):
    submenu_to_update = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id_for_submenu).filter(
        models.Submenu.id == submenu_id).one_or_none()
    if submenu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    else:
        submenu_to_update.title = submen.title
        submenu_to_update.description = submen.description
        db.commit()
        db.refresh(submenu_to_update)
        return submenu_to_update



@app.delete('/api/v1/menus/{menu_id_for_submenu}/submenus/{submenu_id}', response_model=BaseSubmenu)
def delete_submenu(menu_id_for_submenu: int, submenu_id: int):
    smenu_for_delete = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id_for_submenu).filter(
        models.Submenu.id == submenu_id).first()

    if smenu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        # сначала найти блюда привязаненые к этому подменю

        db.delete(smenu_for_delete)
        # ставим счетчик подменю оставшихся
        res = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id_for_submenu).all()
        d = db.query(models.Menu).get(menu_id_for_submenu)
        d.submenus_count = len(res)
        count_dish_for_this_menu = db.query(models.Dish).filter(models.Dish.menu_id == menu_id_for_submenu).all()
        d.dishes_count = len(count_dish_for_this_menu)
        db.add(d)
        db.commit()
        db.refresh(d)
    return smenu_for_delete


###dishes###

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[Dish],
         status_code=status.HTTP_200_OK)
def get_all_dishes(menu_id: int, submenu_id: int):
    dish = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).filter(
        models.Submenu.menu_id == menu_id).all()
    return dish


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=Dish,
         status_code=status.HTTP_200_OK)
def get_one_dishes(menu_id: int, submenu_id: int, dish_id: int):
    dish = db.query(models.Dish).filter(models.Dish.id == dish_id).filter(models.Dish.submenu_id == submenu_id).filter(
        models.Submenu.menu_id == menu_id).one_or_none()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    else:
        return dish


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=Dish,
          status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: int, submenu_id: int, dish: Dish):
    #нужно проверить существуют ли меню и подменю
    new_dish = models.Dish(
        id=str(dish.id or 0),
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
        menu_id=menu_id,
    )
    #проверка на дубликаты
    db_dish = db.query(models.Dish).filter(models.Dish.id==new_dish.id).first()
    menu = db.query(models.Menu).filter(models.Menu.id==menu_id).first()
    submenu = db.query(models.Submenu).filter(models.Submenu.id==submenu_id).first()
    if db_dish is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='dish already exist')
    elif menu is None or submenu is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='menu or submenu not exist')
    else:
        db.add(new_dish)
        db.commit()
        count_dish_submenu = db.query(models.Dish).filter(
            models.Dish.submenu_id == submenu_id).all()
        count_dish_menu = db.query(models.Dish).filter(models.Dish.menu_id == menu_id).all()
        menu_dish = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        submenu_dish = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
        menu_dish.dishes_count = (len(count_dish_menu) + 1)
        submenu_dish.dishes_count = (len(count_dish_submenu) + 1)
        db.add(menu_dish)
        db.add(submenu_dish)
        db.commit()
        db.refresh(menu_dish)
        db.refresh(submenu_dish)
        return new_dish


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=Dish,
           status_code=status.HTTP_200_OK)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: UpgradeDish):
    dish_for_update = db.query(models.Dish).filter(models.Dish.id == dish_id).filter(
        models.Dish.menu_id == menu_id).filter(models.Dish.submenu_id == submenu_id).first()
    if dish_for_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        dish_for_update.title = dish.title
        dish_for_update.description = dish.description
        dish_for_update.price = dish.price
        db.commit()
        db.refresh(dish_for_update)
        return dish_for_update


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
    dish_for_delete = db.query(models.Dish).filter(models.Dish.id == dish_id).filter(
        models.Dish.menu_id == menu_id).filter(models.Dish.submenu_id == submenu_id).first()
    if dish_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        count_dish = db.query(models.Dish).filter(models.Dish.menu_id == menu_id).filter(
            models.Dish.submenu_id == submenu_id).all()
        menu_dish = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        submenu_dish = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish) - 1
        submenu_dish.dishes_count = len(count_dish) - 1
        db.delete(dish_for_delete)
        db.commit()
        return {
            "status": True,
            "message": "The dish has been deleted"
        }
