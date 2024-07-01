from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Discussion, Like, Comment, Hashtag, Follow
import uuid
from sqlalchemy import or_, and_

# from ..get_router import router

post_router = APIRouter()


@post_router.post("/user", status_code=201)
async def create_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["name", "mobile_no", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )
    db_user = (
        db.query(User)
        .filter(or_(User.email == data["email"], User.mobile_no == data["mobile_no"]))
        .first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="User already exits")
    new_user = User(
        name=data["name"],
        mobile_no=data["mobile_no"],
        email=data["email"],
        password=data["password"],
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        HTTPException(status_code=400, detail=str(e))


@post_router.post("/discussion", status_code=201)
async def create_discussion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["text", "user_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )
    hashtags = None
    if data.get("hashtag_ids"):
        hashtags = db.query(Hashtag).filter(Hashtag.id.in_(data["hashtag_ids"])).all()
        if not hashtags:
            raise HTTPException(status_code=400, detail="Invalid hashtag IDs")

    new_discussion = Discussion(
        text=data["text"],
        user_id=data["user_id"],
        image=data.get("image"),
        hashtags=hashtags,
    )

    try:
        db.add(new_discussion)
        db.commit()
        db.refresh(new_discussion)
        return new_discussion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@post_router.post("/hashtag", status_code=201)
async def create_hashtag(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["name"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )

    new_hashtag = Hashtag(name=data["name"])

    try:
        db.add(new_hashtag)
        db.commit()
        db.refresh(new_hashtag)
        return new_hashtag
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@post_router.post("/follow", status_code=201)
async def create_follow(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["user_id", "follow_user_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )

    new_follow = Follow(user_id=data["user_id"], follow_user_id=data["follow_user_id"])

    try:
        db.add(new_follow)
        db.commit()
        db.refresh(new_follow)
        return new_follow
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@post_router.post("/comment", status_code=201)
async def create_comment(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["text", "user_id", "discussion_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )

    new_comment = Comment(
        text=data["text"], user_id=data["user_id"], discussion_id=data["discussion_id"]
    )

    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@post_router.post("/like", status_code=201)
async def create_like(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["user_id", "discussion_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )

    db_like = (
        db.query(Like)
        .filter(
            and_(
                Like.user_id == data["user_id"],
                Like.discussion_id == data["discussion_id"],
            )
        )
        .first()
    )
    if db_like:
        raise HTTPException(
            status_code=400, detail=f"You have already liked this discussion"
        )

    new_like = Like(user_id=data["user_id"], discussion_id=data["discussion_id"])

    try:
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
