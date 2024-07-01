from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Hashtag, Discussion

custom_query_router = APIRouter()


@custom_query_router.get("/user_by_name/{name}")
async def search_user_by_name(name: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.name.ilike(f"%{name}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail=f"User not found")
    return users


@custom_query_router.get("/discussions_by_tag/{tag_id}")
async def get_discussions_by_tag(tag_id: str, db: Session = Depends(get_db)):
    tag = db.query(Hashtag).filter(Hashtag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=404, detail=f"Discussion with Tag ID '{tag_id}' not found"
        )
    discussions = tag.discussions
    return discussions


@custom_query_router.get("/discussions_by_text/{text}")
async def search_discussions_by_text(text: str, db: Session = Depends(get_db)):
    discussions = db.query(Discussion).filter(Discussion.text.ilike(f"%{text}%")).all()
    if not discussions:
        raise HTTPException(status_code=404, detail=f"Discussion not found")
    return discussions
