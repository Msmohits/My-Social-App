from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Discussion, Like, Comment, Hashtag
import uuid

# from ..get_router import router

get_router = APIRouter()


@get_router.get("/")
async def root():
    return {"message": "Hello World"}


@get_router.get("/user/{id}", status_code=200)
async def get_user(id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id).first()
    except Exception as e:
        raise HTTPException(404, str(e))
    if not user:
        raise HTTPException(404, "No user found with this id")
    return user


@get_router.get("/users/", status_code=200)
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
    except Exception as e:
        raise HTTPException(404, str(e))
    if not users:
        raise HTTPException(404, "No user found")
    return users


@get_router.get("/discussion/{id}", status_code=200)
async def get_discussion(id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        discussion = db.query(Discussion).filter(Discussion.id == id).first()
    except Exception as e:
        raise HTTPException(404, str(e))
    if not discussion:
        raise HTTPException(404, "No discussion found with this id")
    return discussion


@get_router.get("/discussions/", status_code=200)
async def get_all_discussions(db: Session = Depends(get_db)):
    try:
        discussions = db.query(Discussion).all()
    except Exception as e:
        raise HTTPException(404, str(e))
    if not discussions:
        raise HTTPException(404, "No discussion found")
    return discussions


@get_router.get("/discussions")
async def get_users(db: Session = Depends(get_db)):
    return db.query(Discussion).all()


@get_router.get("/likes")
async def get_users(db: Session = Depends(get_db)):
    return db.query(Like).all()


@get_router.get("/comments")
async def get_users(db: Session = Depends(get_db)):
    return db.query(Comment).all()


@get_router.get("/hashtags")
async def get_users(db: Session = Depends(get_db)):
    return db.query(Hashtag).all()
