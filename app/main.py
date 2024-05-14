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
from .routers import post, user, auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello World"}
