from fastapi import status
#from httpx import AsyncClient
#import pytest
from my_api.main import app

# id_cur_menu = []

import pytest

@pytest.mark.asyncio
async def test_get_list_menu(async_app_client):
    response = await async_app_client.get("/api/v1/menus")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_root(async_app_client):
    data = {"title": "My menu 1", "description": "My menu description 1"}
    response = await async_app_client.post("/api/v1/menus", json=data)
    assert response.status_code == 201
    r = response.json()
    assert r['title'] == "My menu 1"


@pytest.mark.asyncio
async def test_delete_menu(async_app_client):
    response = await async_app_client.delete("/api/v1/menus/1")
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted",
    }
    assert response.status_code == status.HTTP_200_OK

# @pytest.mark.asyncio
# async def test_get_all_menus():
#     data = {"title": "My menu 1", "description": "My menu description 1"}
#     async with AsyncClient(app=app, base_url='http://test') as ac:
#         response = await ac.post("/api/v1/menus", json=data)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == []


# @pytest.mark.asyncio
# async def test_create_menu():
#     data = {"title": "My menu 1", "description": "My menu description 1"}
#     async with AsyncClient(app=app) as ac:
#         response = await ac.get("/api/v1/menus")
    
#     resp = response.json()
#     assert resp == "My menu 1"
#     # assert resp["id"].isdigit()
#     # assert resp["description"] == "My menu description 1"
#     assert response.status_code == status.HTTP_201_CREATED
#     # id_cur_menu.append(resp["id"])


# def test_one_menu1(client):
#     response = client.get(f"/api/v1/menus/{id_cur_menu[0]}")
#     resp = response.json()
#     assert resp["title"] == "My menu 1"
#     assert resp["id"].isdigit()
#     assert resp["description"] == "My menu description 1"
#     assert response.status_code == status.HTTP_200_OK


# def test_patch_menu(client):
#     response = client.patch(
#         f"/api/v1/menus/{id_cur_menu[0]}",
#         json={
#             "title": "My updated menu 1",
#             "description": "My updated menu description 1",
#         },
#     )
#     res = response.json()
#     assert res["title"] == "My updated menu 1"
#     assert res["description"] == "My updated menu description 1"
#     assert response.status_code == status.HTTP_200_OK


# def test_delete_menu(client):
#     response = client.delete(f"/api/v1/menus/{id_cur_menu[0]}")
#     assert response.json() == {
#         "status": True,
#         "message": "The menu has been deleted",
#     }
#     assert response.status_code == status.HTTP_200_OK
#     id_cur_menu.clear()


# def test_create_menu2(client):
#     response = client.post(
#         "/api/v1/menus",
#         json={"title": "My menu 2", "description": "My menu description 2"},
#     )
#     resp = response.json()
#     assert resp["title"] == "My menu 2"
#     assert resp["id"].isdigit()
#     assert resp["description"] == "My menu description 2"
#     assert response.status_code == status.HTTP_201_CREATED
#     id_cur_menu.append(resp["id"])


# id_submenu = []


# def test_post_sybmenu(client):
#     response = client.post(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus",
#         json={"title": "My submenu 1", "description": "My submenu description 1"},
#     )
#     r = response.json()
#     assert r["title"] == "My submenu 1"
#     assert r["id"].isdigit()
#     assert r["description"] == "My submenu description 1"
#     assert response.status_code == status.HTTP_201_CREATED
#     id_submenu.append(r["id"])


# def test_patch_submenu(client):
#     response = client.patch(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[0]}",
#         json={
#             "title": "My updated submenu 1",
#             "description": "My updated submenu description 1",
#         },
#     )
#     res = response.json()
#     assert res["title"] == "My updated submenu 1"
#     assert res["description"] == "My updated submenu description 1"
#     assert response.status_code == status.HTTP_200_OK


# def test_get_one_sub(client):
#     response = client.get(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[0]}",
#     )
#     res = response.json()
#     assert res["title"] == "My updated submenu 1"
#     assert res["description"] == "My updated submenu description 1"
#     assert response.status_code == status.HTTP_200_OK


# def test_post_sybmenu2(client):
#     response = client.post(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus",
#         json={"title": "My submenu 2", "description": "My submenu description 2"},
#     )
#     r = response.json()
#     assert r["title"] == "My submenu 2"
#     assert r["id"].isdigit()
#     assert r["description"] == "My submenu description 2"
#     assert response.status_code == status.HTTP_201_CREATED
#     id_submenu.append(r["id"])


# def test_delete_submenu(client):
#     response = client.delete(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[1]}",
#     )
#     assert response.json() == {
#         "status": True,
#         "message": "The submenu has been deleted",
#     }
#     assert response.status_code == status.HTTP_200_OK
#     id_submenu.pop(-1)


# id_dish = []


# def testing_add_dish(client):
#     response = client.post(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[0]}/dishes",
#         json={
#             "title": "My dish 1",
#             "description": "My dish description 1",
#             "price": "12.5",
#         },
#     )
#     r = response.json()
#     assert r["title"] == "My dish 1"
#     assert r["description"] == "My dish description 1"
#     assert r["price"] == "12.5"
#     assert response.status_code == status.HTTP_201_CREATED
#     id_dish.append(r["id"])


# def test_patch_dish(client):
#     response = client.patch(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[0]}/dishes/{id_dish[0]}",
#         json={
#             "title": "My updated dish 1",
#             "description": "My updated disch description 1",
#             "price": "12.5",
#         },
#     )
#     res = response.json()
#     assert res["title"] == "My updated dish 1"
#     assert res["description"] == "My updated disch description 1"
#     assert res["price"] == "12.5"
#     assert response.status_code == status.HTTP_200_OK


# def test_delete_dish2(client):
#     response = client.delete(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[0]}/dishes/{id_dish[0]}",
#     )
#     assert response.json() == {
#         "status": True,
#         "message": "The dish has been deleted",
#     }
#     assert response.status_code == status.HTTP_200_OK


# def test_get_all_dish(client):
#     response = client.get(
#         f"/api/v1/menus/{id_cur_menu[0]}/submenus/{id_submenu[0]}/dishes",
#     )
#     assert response.json() == []


# def test_delete_menu3(client):
#     response = client.delete(f"/api/v1/menus/{id_cur_menu[0]}")
#     assert response.json() == {
#         "status": True,
#         "message": "The menu has been deleted",
#     }
#     assert response.status_code == status.HTTP_200_OK
#     id_cur_menu.clear()
#     id_submenu.clear()
#     id_dish.clear()
