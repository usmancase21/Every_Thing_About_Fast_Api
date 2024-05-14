from ..import models, schemas
from fastapi import FastAPI ,Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import database, schemas,models,utils,oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
# @router.get("/")
# def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]= ""):
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     # print(posts)
#     # print(limit)
#     # print(search)
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
#     print(results)
#     # return posts
#     return results

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]= ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Convert the query result to a list of dictionaries
    results = [{"post": post, "votes": votes} for post, votes in results]
    
    return results
    # return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

#     print(current_user.id)
#     new_post = models.Post(owner_id=current_user.id,**post.model_dump())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the Id {id} was not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the Id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
  
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the Id {id} was not found")
    # post_query.update({'title':"this is my updated title", 'content':"this is my update content"}, synchronize_session=False)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    
    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()


