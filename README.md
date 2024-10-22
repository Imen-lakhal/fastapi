# Backend Clone of Social Media App Using FastAPI

This API has 4 main routes:

### 1) Post Route

This route is responsible for:
- Creating posts
- Deleting posts
- Updating posts
- Checking posts

### 2) Users Route

This route is about:
- Creating users
- Searching users by ID

### 3) Auth Route

This route handles the login system and user authentication.

### 4) Vote Route

This route is about:
- Likes or votes on posts
- Contains code for upvoting (currently no downvote logic)

## How to Run Locally

To run this project locally, follow these steps:

1. Clone this repository:

```bash
git clone https://github.com/Imen-lakhal/fastapi.git
```

Then install fastapp using all flag like

```bash
pip install fastapi[all]
```

Then go this repo folder in your local computer run follwoing command

```bash
uvicorn App.main:app --reload
```

Then you can use following link to use the API

```bash
http://127.0.0.1:8000/docs 
```

## After run this API you need a database in postgres

Create a database in postgres then create a file name .env and write the following things in you file
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = get_key_for_youself
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
