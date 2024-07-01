from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Discussion, Like, Comment, Hashtag, Follow
import uuid
from sqlalchemy import or_, and_

# from ..get_router import router

put_router = APIRouter()


@put_router.put("/user/{user_id}", status_code=200)
async def update_user(
    user_id: uuid.UUID, request: Request, db: Session = Depends(get_db)
):
    data = await request.json()

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found with given ID")

        for field, value in data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@put_router.put("/discussion/{discussion_id}", status_code=200)
async def update_discussion(
    discussion_id: uuid.UUID, request: Request, db: Session = Depends(get_db)
):
    data = await request.json()

    try:
        discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
        if not discussion:
            raise HTTPException(status_code=404, detail="Discussion not found")

        for field, value in data.items():
            setattr(discussion, field, value)

        db.commit()
        db.refresh(discussion)
        return discussion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@put_router.put("/hashtag/{hashtag_id}", status_code=200)
async def update_hashtag(
    hashtag_id: uuid.UUID, request: Request, db: Session = Depends(get_db)
):
    data = await request.json()

    try:
        hashtag = db.query(Hashtag).filter(Hashtag.id == hashtag_id).first()
        if not hashtag:
            raise HTTPException(status_code=404, detail="Hashtag not found")

        for field, value in data.items():
            setattr(hashtag, field, value)

        db.commit()
        db.refresh(hashtag)
        return hashtag
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@put_router.put("/comment/{comment_id}", status_code=200)
async def update_comment(
    comment_id: uuid.UUID, request: Request, db: Session = Depends(get_db)
):
    data = await request.json()

    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        for field, value in data.items():
            setattr(comment, field, value)

        db.commit()
        db.refresh(comment)
        return comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@put_router.put("/like/{like_id}", status_code=200)
async def update_like(
    like_id: uuid.UUID, request: Request, db: Session = Depends(get_db)
):
    data = await request.json()

    try:
        like = db.query(Like).filter(Like.id == like_id).first()
        if not like:
            raise HTTPException(status_code=404, detail="Like not found")

        for field, value in data.items():
            setattr(like, field, value)

        db.commit()
        db.refresh(like)
        return like
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@put_router.put("/follow/{follow_id}", status_code=200)
async def update_follow(
    follow_id: uuid.UUID, request: Request, db: Session = Depends(get_db)
):
    data = await request.json()

    try:
        follow = db.query(Follow).filter(Follow.id == follow_id).first()
        if not follow:
            raise HTTPException(status_code=404, detail="Follow not found")

        for field, value in data.items():
            setattr(follow, field, value)

        db.commit()
        db.refresh(follow)
        return follow
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
