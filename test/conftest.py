from fastapi.testclient import TestClient
import pytest 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from App.main import app
from App.config import settings
from App.database import get_db
from App.database import Base
from App import models
from App.oauth2 import create_access_token


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:i53480951@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'



engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("my session fixture ran ")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #yield: We should use yield when we want to iterate over a sequence, but don't want to store the entire sequence in memory.

@pytest.fixture
def test_user2(client):
    user_data = {"email": "fathiya@gmail.com",
                 "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email":"imen@gmail.com",
                 "password":"password"}
    res= client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user= res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "name": "first title",
        "mail": "first content",
        "owner_id": test_user['id']
    }, {
        "name": "2nd title",
        "mail": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "name": "3rd title",
        "mail": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "name": "3rd title",
        "mail": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts