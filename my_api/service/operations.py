from fastapi import Depends, HTTPException, status
from ..db.database import get_db
from ..models_schemas import schemas
import my_api.cache_op.cache_operations as cache
from ..models_schemas.models import Menu, Submenu, Dish
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class MenuCrud:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session
        
        
    async def get_list(self):
        """Возвращает список всех меню1"""
        q = select(Menu)
        res = await self.session.execute(q)
        menu = res.scalars().all()
        cache.cache_list_item(menu, 'menulist')
        return menu
    
    async def get_one_menu(self, menu_id: int) -> schemas.BaseMenu:
        """Возвращает меню по его id"""
        q = select(Menu).where(Menu.id == menu_id)
        res = await self.session.execute(q)
        menu = res.scalar_one_or_none()
        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        cache.cache_item(id_item=menu_id, item=menu, type="menu")
        return menu
    
    
    async def create_menu_table(self, menu: schemas.CreateMenu) -> Menu:
        """Создает обьект меню"""
        new_menu = Menu(
        title=menu.title,
        description=menu.description,
        )
        self.session.add(new_menu)
        return new_menu


    async def create_menu(self, menu: schemas.CreateMenu) -> schemas.BaseMenu:
        """Создает меню в базе данных"""
        new_menu = await self.create_menu_table(menu=menu)
        try:
            await self.session.commit()
            return new_menu
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="menu already exist")


    async def update_menu(
        self,
        menu_id: int,
        menu: schemas.CreateMenu,
        ) -> schemas.BaseMenu:
        """Обновляет меню по id"""
        menu_to_update = await self.get_one_menu(menu_id=menu_id)
        if menu_to_update:
            menu_to_update.id = menu_id
            menu_to_update.title = menu.title
            menu_to_update.description = menu.description
            await self.session.commit()
            await self.session.refresh(menu_to_update)
            return menu_to_update
        return menu_to_update
    
    async def delete_menu(self, menu_id: int) -> dict:
        """Удаляет меню по id"""
        menu_for_delete = await self.get_one_menu(menu_id=menu_id)
        if menu_for_delete:
            await self.session.delete(menu_for_delete)
            await self.session.commit()
            return {"status": True, "message": "The menu has been deleted"}
        return menu_for_delete
    
    
class SubmenuCrud:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session
        
    async def count_submenu(self, id) -> list[schemas.BaseSubmenu]:
        """Находит количество всех подменю по id заданного меню"""
        q = select(Submenu).where(Submenu.menu_id == id)
        res = await self.session.execute(q)
        submenus = res.scalars().all()
        cache.cache_list_item(submenus, 'submenulist')
        return submenus
    
    async def get_one_submenu_by_id(
        self,
        menu_id: int,
        submenu_id: int,
    ) -> schemas.BaseSubmenu:
        """Возвращает конкретное подменю по id меню и подменю"""
        q = select(Submenu).where(Submenu.menu_id == menu_id).where(Submenu.id == submenu_id)
        res = await self.session.execute(q)
        one_submenu = res.scalar_one_or_none()
        if one_submenu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        else:
            cache.cache_item(id_item=submenu_id, item=one_submenu, type="submenu")
            return one_submenu


    async def get_submenu_list(self, menu_id: int) -> list[schemas.BaseSubmenu]:
        """Возврашает список всех подменю по id меню"""
        all_s_menu = await self.count_submenu(id=menu_id)
        #cache.cache_list_item(array=all_s_menu, type="list_submenu")
        return all_s_menu
    
    
    async def create_submenu_table(self,
        menu_id: int,
        sub: schemas.CreateSubmenu,
    ) -> Submenu:
        """Создает обьект подменю"""
        new_submenu = Submenu(
            title=sub.title,
            description=sub.description,
            menu_id=menu_id,
        )
        self.session.add(new_submenu)
        return new_submenu


    async def create_submenu(
        self,
        menu_id: int,
        sub: schemas.CreateSubmenu,
    ) -> schemas.BaseSubmenu:
        """Создание подменю в бвзе данных"""
        new_submenu = await self.create_submenu_table(menu_id=menu_id, sub=sub)
        res = await self.session.execute(select(Menu).where(Menu.id == menu_id))
        menu = res.scalar_one()
        count_s = await self.count_submenu(menu_id)
        try:
            menu.submenus_count = len(count_s)
            await self.session.commit()
            return new_submenu
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="submenu already exist")
        
    async def update_submenu(
        self,
        menu_id: int,
        submenu_id: int,
        submenu: schemas.CreateSubmenu,
        ) -> schemas.BaseSubmenu:
        """Обновление подменю по id меню и подменю"""
        submenu_to_update = await self.get_one_submenu_by_id(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if submenu_to_update is None:
            return submenu_to_update
        else:
            submenu_to_update.title = submenu.title
            submenu_to_update.description = submenu.description
            await self.session.commit()
            await self.session.refresh(submenu_to_update)
            return submenu_to_update
        
    async def delete_submenu(self, menu_id: int, submenu_id: int) -> dict:
        """Удаление подменю"""
        s_menu_for_delete = await self.get_one_submenu_by_id(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if s_menu_for_delete is None:
            return s_menu_for_delete
        else:
            count_sub = await self.count_submenu(id=menu_id)
            res = await self.session.execute(select(Menu).where(Menu.id == menu_id))
            menu = res.scalar_one()
            menu.submenus_count = len(count_sub) - 1
            await self.session.delete(s_menu_for_delete)
            await self.session.commit()
            await self.session.refresh(menu)
            res = await self.session.execute(select(Dish).where(Dish.menu_id == menu_id))
            count_dish_for_this_menu = res.scalars().all()
            menu.dishes_count = len(count_dish_for_this_menu)
            await self.session.commit()
            await self.session.refresh(menu)
            return {"status": True, "message": "The submenu has been deleted"}
        
        
class DishCrud:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session
    
    
    async def get_all_dishes(
        self,
        menu_id: int,
        submenu_id: int,
    ) -> list[schemas.BaseDish]:
        """Возвращает список всех блюд по id меню и подменю"""
        res = await self.session.execute(select(Dish).where(Dish.menu_id==menu_id).where(Dish.submenu_id == submenu_id))
        dish = res.scalars().all()
        cache.cache_list_item(array=dish, type="list_dish")
        return dish
    
    
    async def get_one_dishes(
        self,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
    ) -> schemas.BaseDish:
        """Возвращает конкретное блюдо по id меню, подменю и блюда"""
        res = await self.session.execute(select(Dish).where(Dish.menu_id==menu_id).where(Dish.submenu_id == submenu_id).where(Dish.id == dish_id))
        dish = res.scalar_one_or_none()
        if dish is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        else:
            cache.cache_item(item=dish, id_item=dish_id, type="dish")
            return dish
        
        
    async def create_dish_table(self, menu_id: int, submenu_id: int, dish: schemas.CreateDish) -> Dish:
        """Создание объекта типа блюдо"""
        new_dish = Dish(
            title=dish.title,
            description=dish.description,
            price=float(dish.price),
            submenu_id=submenu_id,
            menu_id=menu_id,
        )
        self.session.add(new_dish)
        return new_dish


    def count_dish_for_menu(self, menu_id) -> list[schemas.BaseDish]:
        """Возвращает список всех блюд по меню id"""
        return self.session.query(Dish).filter(Dish.menu_id == menu_id).all()
    
    
    async def create_dish(
        self,
        menu_id: int,
        submenu_id: int,
        dish: schemas.CreateDish,
    ) -> schemas.BaseDish:
        """Создание блюда"""
        
        new_dish = await self.create_dish_table(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish=dish,
        )
        res = await self.session.execute(select(Menu).where(Menu.id == menu_id))
        menu = res.scalar_one_or_none()
        res2 = await self.session.execute(select(Submenu).where(Submenu.id == submenu_id))
        submenu = res2.scalar_one_or_none()
        if menu is None or submenu is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="menu or submenu not exist",
            )
        else:
            try:
                #await self.session.commit()
                q1 = await self.session.execute(select(Dish).where(Dish.menu_id == menu_id))
                count_dish_menu = q1.scalars().all()
                q2 = await self.session.execute(select(Dish).where(Dish.submenu_id == submenu_id))
                count_dish_submenu = q2.scalars().all()
                menu.dishes_count = len(count_dish_menu)
                submenu.dishes_count = len(count_dish_submenu)
                await self.session.commit()
                return new_dish
            except Exception as e:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dish already exist",
                )
    
    
    async def update_dish(
        self,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish: schemas.CreateDish,
    ) -> schemas.BaseDish:
        """Обновление блюда по id меню, подменю и блюда"""
        q = select(Dish).where(Dish.id == dish_id).where(Dish.menu_id == menu_id).where(Dish.submenu_id == submenu_id)
        res = await self.session.execute(q)
        dish_for_update = res.scalar_one()
        if dish_for_update is None:
            return dish_for_update
        else:
            dish_for_update.title = dish.title
            dish_for_update.description = dish.description
            dish_for_update.price = float(dish.price)
            await self.session.commit()
            await self.session.refresh(dish_for_update)
            return dish_for_update
        

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> dict:
        """Удаление блюда"""
        q = select(Dish).where(Dish.id == dish_id).where(Dish.menu_id == menu_id).where(Dish.submenu_id == submenu_id)
        res = await self.session.execute(q)
        dish_for_delete = res.scalar_one()
        q1 = await self.session.execute(select(Menu).where(Menu.id == menu_id))
        menu_dish = q1.scalar_one()
        q2 = await self.session.execute(select(Submenu).where(Submenu.id == submenu_id))
        submenu_dish = q2.scalar_one()
        if dish_for_delete is None:
            return dish_for_delete
        else:
            count_dish = await self.get_all_dishes(
                menu_id=menu_id,
                submenu_id=submenu_id,
            )
            menu_dish.dishes_count = len(count_dish) - 1
            submenu_dish.dishes_count = len(count_dish) - 1
            await self.session.delete(dish_for_delete)
            await self.session.commit()
            await self.session.refresh(menu_dish)
            await self.session.refresh(submenu_dish)
            return {"status": True, "message": "The dish has been deleted"}
