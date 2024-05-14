from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from fastapi import Response, status,HTTPException, Depends
from . import models,schemas,utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Response, status,HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import time
from passlib.context import CryptContext
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='u8256266' ,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successfull!")
        break
    except Exception as e:
        print("Connection to database failed")
        print("Error",e)
        time.sleep(2)

my_posts = [
    {"title": "My First Post","content": "This is the content of my first post","id":1,},
    {"title": "My Second Post","content": "This is the content of my second post","id":2,},
]

def find_post(id):
    for p in my_posts:
        if p['id'] ==id:
            return p

def find_index_post(id:int):
    for i,p in enumerate(my_posts):
        if p["id"] ==id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Hello World"}
