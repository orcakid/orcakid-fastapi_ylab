def test_get_all_menus(client):
    response = client.get('/api/v1/menus')
    assert response.json() == []
    assert response.status_code == 200 
    


def test_one_menu(client):
    response = client.get('/api/v1/menus/0')
    assert response.json() == {'detail': 'menu not found'}
    
        

def test_create_menu(client):
    response = client.post('/api/v1/menus', json={'title': 'My menu 1', 'description': 'My menu description 1'})
    assert response.json() == {
        "id": 0,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
        }

    

def test_one_menu1(client):
    response = client.get('/api/v1/menus/0')
    assert response.json() == {
        "id": 0,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
        }

def test_patch_menu(client):
    response = client.patch('/api/v1/menus/0', json={'title': 'My updated menu 2', 'description': 'My updated menu description 2'})
    assert response.json() == {
        "id": 0,
        "title": "My updated menu 2",
        "description": "My updated menu description 2",
        "submenus_count": 0,
        "dishes_count": 0
        }
    
    
def test_delete_menu(client):
    response = client.delete('/api/v1/menus/0')
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted"
    }
    

def test_patch_menu_when_delete(client):
    response = client.patch('/api/v1/menus/1', json={'title': 'My updated menu 1', 'description': 'My updated menu description 1'})
    assert response.json() == {'detail': 'menu not found'}
    

def test_delete_menu(client):
    response = client.delete('/api/v1/menus/3')
    assert response.json() == { "detail": "Not Found"}
    

def test_create_menu(client):
    response = client.post('/api/v1/menus', json={'title': 'My menu 1', 'description': 'My menu description 1'})
    assert response.json() == {
        "id": 0,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
        }


def test_get_sub(client):
    response = client.get('/api/v1/menus/0/submenus')
    assert response.json() == []
    

def test_post_sybmenu(client):
    response = client.post('/api/v1/menus/0/submenus', json={'title': 'My submenu 1', 'description': 'My submenu description 1'})
    assert response.json() == {
        "id": 0,
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 0
        }
    

def test_get_sub_one_not(client):
    response = client.get('/api/v1/menus/0/submenus/1')
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
    
    
    
def test_patch_sybmenu(client):
    response = client.patch('/api/v1/menus/0/submenus/0', json={'title': 'My update submenu 1', 'description': 'My update submenu description 1'})
    assert response.json() == {
        "id": 0,
        "title": "My update submenu 1",
        "description": "My update submenu description 1",
        "dishes_count": 0
        }
    

def test_del_submenu(client):
    response = client.delete('/api/v1/menus/0/submenus/0')
    assert response.json() == {
        "status": True,
        "message": "The submenu has been deleted"
    }


def test_post_sybmenu1(client):
    response = client.post('/api/v1/menus/0/submenus', json={'title': 'My submenu 1',
                                                            'description': 'My submenu description 1'})
    assert response.json() == {
        "id": 0,
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 0
        }
    

def test_get_list_dishes(client):
    responce = client.get('/api/v1/menus/1/submenus/0/dishes')
    assert responce.json() == []
    

def testing_add_dish(client):
    response = client.post('/api/v1/menus/0/submenus/0/dishes', json={"title": "My dish 1",
                                                                    "description": "My dish description 1",
                                                                    "price": "12.5"})
    assert response.json() == {
        "id": 0,
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.5"
    }
    

def test_patch_dish(client):
    response = client.patch('/api/v1/menus/0/submenus/0/dishes/0', json={"title": "My updated dish 1",
                                                                    "description": "My updated dish description 1",
                                                                    "price": "14.5"})
    assert response.json() == {
        "id": 0,
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.5"
    }


def test_get_one_dish(client):
    response = client.get('/api/v1/menus/0/submenus/0/dishes/0')
    assert response.json() == {
        "id": 0,
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.5"
    }


    
def test_delete_dish_empty(client):
    response = client.get('/api/v1/menus/0/submenus/0/dishes/3')
    assert response.json() == {
        "detail": "dish not found"
    }
    

def test_delete_menu1(client):
    response = client.delete('/api/v1/menus/0')
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted"
    }
    


    
