from .. import models,schemas
from typing import List, Optional
from fastapi import FastAPI,Response, status,HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts" 
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.name.contains(search)).limit(limit).offset(skip).all()
    return posts
 
'''
@router.get("/posts", response_model=List[schemas.Post])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts =  cursor.fetchall()
    return posts 
'''

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post:schemas.PostCreate,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_one= models.Post(owner_id=current_user.id , **new_post.dict())
    #new_one= models.Post(name=new_post.name, mail= new_post.mail, published=new_post.published)
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one

'''
@router.post("/posts",  response_model=schemas.Post)
#def create_posts(payLoad: dict = Body(...)):
def create_posts(new_post:schemas.PostCreate):
    #print(new_post)
    #print(new_post.name)
    #post_dict=new_post.dict()
    #post_dict['id'] = randrange(0,1000000)
    #print(new_post.dict())
    #my_posts.append(post_dict)
    #return {"message":post_dict} 
    cursor.execute("""INSERT INTO posts (name,mail,published) VALUES (%s,%s,%s) RETURNING * """,(new_post.name,new_post.mail,new_post.published))
    new_one = cursor.fetchone()
    conn.commit()
    return new_one
'''



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post

'''    
@router.get("/posts/{id}", response_model=schemas.Post)
def get_posts(id:int,response: Response):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    print(post)
    #post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message":"id not found"}
    return post
'''


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id not found")
    
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


'''
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("""DELETE from posts WHERE id = %s returning * """, (str(id),))
    deleted_post= cursor.fetchone()
    #index =find_index_post(id)
    conn.commit()
    if deleted_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id not found")
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
'''

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id:int, post:schemas.PostCreate,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    updated_post=post_query.first()

    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id not found")
    
    if updated_post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()



'''
@router.put("/posts/{id}", response_model=schemas.Post)
def update_posts(id:int, post:schemas.PostCreate):
    cursor.execute("""UPDATE posts set name=%s , mail=%s , published=%s WHERE id = %s returning *""", (post.name, post.mail, post.published, str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    #index =find_index_post(id)

    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id not found")
    
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return updated_post
'''