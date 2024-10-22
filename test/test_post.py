import pytest
from App import schemas
from App.config import settings

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
 
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.name == test_posts[0].name
    assert post.Post.mail == test_posts[0].mail


@pytest.mark.parametrize("name, mail, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, name, mail, published):
    res = authorized_client.post(
        "/posts/", json={"name": name, "mail": mail, "published": published})

    created_post = schemas.Post(**res.json())
    print(created_post)
    assert res.status_code == 201
    assert created_post.name == name
    assert created_post.mail == mail
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"name": "hi", "mail": "helloo"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.name == "hi"
    assert created_post.mail == "helloo"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"name": "hi", "mail": "helloo"})
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "name": "updated title",
        "mail": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.name == data['name']
    assert updated_post.mail == data['mail']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "name": "updated title",
        "mail": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "name": "updated title",
        "mail": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404


def test_port ():
    assert settings.database_port == 5432 

def test_token():
    assert settings.access_token_expire_minutes == 30