from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models_schemas import schemas
import my_api.cache_op.cache_operations as cache
from ..models_schemas.models import Menu, Submenu, Dish


class MenuCrud:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        

    def get_list_menu(self) -> list[schemas.BaseMenu]:
        """Возвращает список всех меню1"""
        menu = self.session.query(Menu).all()
        cache.cache_list_item(array=menu, type="list_menu")
        return menu
    
    
    def get_one_menu(self, menu_id: int) -> schemas.BaseMenu:
        """Возвращает меню по его id"""
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        cache.cache_item(id_item=menu_id, item=menu, type="menu")
        return menu
    
    
    def create_menu_table(self, menu: schemas.CreateMenu) -> Menu:
        """Создает обьект меню"""
        new_menu = Menu(
        title=menu.title,
        description=menu.description,
        )
        return new_menu


    def chehing_exist(self, title_menu, new_menu: Menu) -> Menu:
        """Проверяет на существование одинакового меню и добавляет"""
        menu_db = self.session.query(Menu).filter(Menu.title == title_menu).first()
        if menu_db is None:
            self.session.add(new_menu)
            self.session.commit()
            return new_menu
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="menu already exist",
            )


    def create_menu(self, menu: schemas.CreateMenu) -> schemas.BaseMenu:
        """Создает меню в базе данных"""
        new_menu = self.create_menu_table(menu=menu)
        check = self.chehing_exist(title_menu=menu.title, new_menu=new_menu)
        return check
    
    
    def update_menu(
        self,
        menu_id: int,
        menu: schemas.CreateMenu,
        ) -> schemas.BaseMenu:
        """Обновляет меню по id"""
        menu_to_update = self.get_one_menu(menu_id=menu_id)
        if menu_to_update:
            menu_to_update.id = menu_id
            menu_to_update.title = menu.title
            menu_to_update.description = menu.description
            self.session.commit()
            self.session.refresh(menu_to_update)
            return menu_to_update
        return menu_to_update
    
    def delete_menu(self, menu_id: int) -> dict:
        """Удаляет меню по id"""
        menu_for_delete = self.get_one_menu(menu_id=menu_id)
        if menu_for_delete:
            self.session.delete(menu_for_delete)
            self.session.commit()
            return {"status": True, "message": "The menu has been deleted"}
        return menu_for_delete
    
    
class SubmenuCrud:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        
    def count_submenu(self, id) -> list[schemas.BaseSubmenu]:
        """Находит количество всех подменю по id заданного меню"""
        return self.session.query(Submenu).filter(Submenu.menu_id == id).all()
    
    def get_one_submenu_by_id(
        self,
        menu_id: int,
        submenu_id: int,
    ) -> schemas.BaseSubmenu:
        """Возвращает конкретное подменю по id меню и подменю"""
        one_submenu = (
            self.session.query(Submenu)
            .filter(Submenu.menu_id == menu_id)
            .filter(
                Submenu.id == submenu_id,
            )
            .first()
        )
        if one_submenu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        else:
            cache.cache_item(id_item=submenu_id, item=one_submenu, type="submenu")
            return one_submenu


    def get_submenu_list(self, menu_id: int) -> list[schemas.BaseSubmenu]:
        """Возврашает список всех подменю по id меню"""
        all_s_menu = self.session.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        cache.cache_list_item(array=all_s_menu, type="list_submenu")
        return all_s_menu
    
    def count_dish_for_submenu(self, id_sub) -> list[schemas.BaseDish]:
        """Находит количество блюд по id подменю"""
        return self.session.query(Dish).filter(Dish.submenu_id == id_sub).all()
    
    def create_submenu_table(self,
        menu_id: int,
        sub: schemas.CreateSubmenu,
    ) -> Submenu:
        """Создает обьект подменю"""
        new_submenu = Submenu(
            title=sub.title,
            description=sub.description,
            menu_id=menu_id,
        )
        return new_submenu
    
    def checking_submenu(self, sub_title, new_submenu) -> schemas.BaseSubmenu:
        """Проверка на существование такого же подменю и добавление его в бд"""
        db_sub = self.session.query(Submenu).filter(Submenu.title == sub_title).first()
        if db_sub is None:
            self.session.add(new_submenu)
            self.session.commit()
            return new_submenu
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="menu already exist",
            )
            
    def create_submenu(
        self,
        menu_id: int,
        sub: schemas.CreateSubmenu,
    ) -> schemas.BaseSubmenu:
        """Создание подменю в бвзе данных"""
        new_submenu = self.create_submenu_table(menu_id=menu_id, sub=sub)
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if menu:
            submenu = self.checking_submenu(
                sub_title=new_submenu.title,
                new_submenu=new_submenu,
            )
            # учет количества сабменю в данном меню
            count_sub = self.count_submenu(id=menu_id)
            if count_sub is not None:
                d = self.session.query(Menu).filter(Menu.id == menu_id).first()
                d.submenus_count = len(count_sub)
                self.session.add(d)
                self.session.commit()
            return submenu
        
    def update_submenu(
        self,
        menu_id: int,
        submenu_id: int,
        submenu: schemas.CreateSubmenu,
        ) -> schemas.BaseSubmenu:
        """Обновление подменю по id меню и подменю"""
        submenu_to_update = self.get_one_submenu_by_id(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if submenu_to_update is None:
            return submenu_to_update
        else:
            submenu_to_update.title = submenu.title
            submenu_to_update.description = submenu.description
            self.session.commit()
            self.session.refresh(submenu_to_update)
            return submenu_to_update
        
    def delete_submenu(self, menu_id: int, submenu_id: int) -> dict:
        """Удаление подменю"""
        s_menu_for_delete = self.get_one_submenu_by_id(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if s_menu_for_delete is None:
            return s_menu_for_delete
        else:
            count_sub = self.count_submenu(id=menu_id)
            menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
            menu.submenus_count = len(count_sub) - 1
            self.session.delete(s_menu_for_delete)
            self.session.commit()
            self.session.refresh(menu)
            count_dish_for_this_menu = self.session.query(Dish).filter(Dish.menu_id == menu_id).all()
            menu.dishes_count = len(count_dish_for_this_menu)
            self.session.commit()
            self.session.refresh(menu)
            return {"status": True, "message": "The submenu has been deleted"}
        
        
class DishCrud:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
    
    
    def get_all_dishes(
        self,
        menu_id: int,
        submenu_id: int,
    ) -> list[schemas.BaseDish]:
        """Возвращает список всех блюд по id меню и подменю"""
        dish = (
            self.session.query(Dish)
            .filter(Dish.menu_id == menu_id)
            .filter(Dish.submenu_id == submenu_id)
            .all()
        )
        cache.cache_list_item(array=dish, type="list_dish")
        return dish if dish else []
    
    
    def get_one_dishes(
        self,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
    ) -> schemas.BaseDish:
        """Возвращает конкретное блюдо по id меню, подменю и блюда"""
        dish = (
            self.session.query(Dish)
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
                detail="dish not found",
            )
        else:
            cache.cache_item(item=dish, id_item=dish_id, type="dish")
            return dish
        
        
    def create_dish_table(self, menu_id: int, submenu_id: int, dish: schemas.CreateDish) -> Dish:
        """Создание объекта типа блюдо"""
        new_dish = Dish(
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id,
            menu_id=menu_id,
        )
        return new_dish


    def checking_dish(self, dish: schemas.CreateDish, new_dish) -> schemas.BaseDish:
        """Проверка и добавление в бд обьекта типа блюдо"""
        db_dish = self.session.query(Dish).filter(Dish.title == dish.title).first()
        if db_dish is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dish already exist",
            )
        else:
            self.session.add(new_dish)
            self.session.commit()
            return new_dish
        

    def count_dish_for_menu(self, menu_id) -> list[schemas.BaseDish]:
        """Возвращает список всех блюд по меню id"""
        return self.session.query(Dish).filter(Dish.menu_id == menu_id).all()
    
    
    def create_dish(
        self,
        menu_id: int,
        submenu_id: int,
        dish: schemas.CreateDish,
    ) -> schemas.BaseDish:
        """Создание блюда"""
        new_dish = self.create_dish_table(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish=dish,
        )
        menu = self.session.query(Menu).filter(Menu.id==menu_id).first()
        submenu = self.session.query(Submenu).filter(Submenu.id==submenu_id).first()
        if menu is None or submenu is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="menu or submenu not exist",
            )
        db_dish = self.checking_dish(dish=new_dish, new_dish=new_dish)
        count_dish_submenu = self.session.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        count_dish_menu = self.count_dish_for_menu(menu_id=menu_id)

        menu.dishes_count = len(count_dish_menu)
        submenu.dishes_count = len(count_dish_submenu)
        self.session.add(menu)
        self.session.add(submenu)
        self.session.commit()
        self.session.refresh(menu)
        self.session.refresh(submenu)
        return db_dish
    
    
    def update_dish(
        self,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish: schemas.CreateDish,
    ) -> schemas.BaseDish:
        """Обновление блюда по id меню, подменю и блюда"""
        dish_for_update = self.get_one_dishes(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        if dish_for_update is None:
            return dish_for_update
        else:
            dish_for_update.title = dish.title
            dish_for_update.description = dish.description
            dish_for_update.price = dish.price
            self.session.commit()
            self.session.refresh(dish_for_update)
            return dish_for_update
        

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> dict:
        """Удаление блюда"""
        dish_for_delete = self.get_one_dishes(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        if dish_for_delete is None:
            return dish_for_delete
        else:
            count_dish = self.get_all_dishes(
                menu_id=menu_id,
                submenu_id=submenu_id,
            )

            menu_dish = self.session.query(Menu).filter(Menu.id==menu_id).first()
            submenu_dish = self.session.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
            menu_dish.dishes_count = len(count_dish) - 1
            submenu_dish.dishes_count = len(count_dish) - 1
            self.session.delete(dish_for_delete)
            self.session.commit()
            return {"status": True, "message": "The dish has been deleted"}