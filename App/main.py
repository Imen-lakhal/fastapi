from fastapi import  FastAPI
from . import models
from .database import engine, get_db
from .router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)



app = FastAPI()

#ay domain tnajam tahki bih ma3 api
origins= ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



'''
my_posts=[{"name":"imen","mail":"imen@gmail.com","id":1}, {"name":"mokhles","mail":"mokhles@gmail.com","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id :
            return p
        



def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id :
            return i
'''


@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)








