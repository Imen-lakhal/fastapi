from fastapi.testclient import TestClient
from App.main import app
import pytest # type: ignore
from App import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from App.config import settings
from App.database import get_db
from App.database import Base
from jose import jwt
from App.config import settings




def test_root(client):
    res= client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    

def test_create_user(client):
    res = client.post("/users/", json={"email":"ons@gmail.com", "password":"password"})
    new_user = schemas.UserOut(**res.json())
    print(new_user)

    #print(res.json())
    #assert new_user.email=="haroun@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
 

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'