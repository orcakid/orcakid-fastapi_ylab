from typing import List

from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from database import Session_local, get_db
from schemas import BaseMenu, BaseSubmenu, PatchMenu, BaseDish, PatchSubmenu, CreateMenu, CreateSubmenu, CreateDish
import crud as crud


router = APIRouter()


@router.get('/api/v1/menus', response_model=List[BaseMenu])
def get_menus(db: Session=Depends(get_db)):
    _menu = crud.get_all_menus(db=db)
    return _menu


@router.get('/api/v1/menus/{menu_id}', response_model=BaseMenu)
def get_one_menu(menu_id: int, db: Session=Depends(get_db)):
    return crud.get_menu(db=db, menu_id=menu_id)


@router.post('/api/v1/menus', response_model=BaseMenu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: CreateMenu, db: Session=Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)


@router.patch('/api/v1/menus/{menu_id}', response_model=BaseMenu)
def update_menu(menu_id: int, menu: PatchMenu, db: Session=Depends(get_db)):
    return crud.update_menu(db=db, menu=menu, menu_id=menu_id)


@router.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: int, db: Session=Depends(get_db)):
    return crud.delete_menu(db=db, menu_id=menu_id)


@router.get('/api/v1/menus/{menu_id}/submenus', response_model=List[BaseSubmenu])
def get_list_submenu(menu_id: int, db: Session=Depends(get_db)):
    return crud.get_submenu_list(db=db, menu_id=menu_id)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=BaseSubmenu)
def get_one_submenu(menu_id: int, submenu_id: int, db: Session=Depends(get_db)):
    return crud.get_one_submenu_of_menu_by_id(db=db, menu_id=menu_id, submenu_id=submenu_id)
    
    
@router.post('/api/v1/menus/{menu_id}/submenus', response_model=BaseSubmenu, status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: int, sub: CreateSubmenu, db: Session=Depends(get_db)):
    return crud.create_submenu(db=db, menu_id=menu_id, sub=sub)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=BaseSubmenu)
def update_submenu(menu_id: int, submenu_id: int, sub: PatchSubmenu, db: Session=Depends(get_db)):
    return crud.update_submenu(db=db, submenu_id=submenu_id, menu_id=menu_id, submenu=sub)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: int, submenu_id: int, db: Session=Depends(get_db)):
    return crud.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    
    
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[BaseDish])
def get_dishes_list(menu_id: int, submenu_id: int, db: Session=Depends(get_db)):
    return crud.get_all_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id)
    

@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=BaseDish)
def get_one_dishes(menu_id: int, submenu_id: int, dish_id: int, db: Session=Depends(get_db)):
    return crud.get_one_dishes(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=BaseDish, status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: int, submenu_id: int, dish: CreateDish, db: Session=Depends(get_db)):
    return crud.create_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish=dish)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',response_model=BaseDish)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: BaseDish, db: Session=Depends(get_db)):
    return crud.update_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dish=dish)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session=Depends(get_db)):
    return crud.delete_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)