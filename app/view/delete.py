from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Discussion, Like, Comment, Hashtag, Follow
import uuid

delete_router = APIRouter()


@delete_router.delete("/user/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}


@delete_router.delete("/discussion/{discussion_id}", status_code=204)
def delete_discussion(discussion_id: uuid.UUID, db: Session = Depends(get_db)):
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    db.delete(discussion)
    db.commit()
    return {"message": f"Discussion with ID {discussion_id} deleted successfully"}


@delete_router.delete("/hashtag/{hashtag_id}", status_code=204)
def delete_hashtag(hashtag_id: uuid.UUID, db: Session = Depends(get_db)):
    hashtag = db.query(Hashtag).filter(Hashtag.id == hashtag_id).first()
    if not hashtag:
        raise HTTPException(status_code=404, detail="Hashtag not found")
    db.delete(hashtag)
    db.commit()
    return {"message": f"Hashtag with ID {hashtag_id} deleted successfully"}


@delete_router.delete("/comment/{comment_id}", status_code=204)
def delete_comment(comment_id: uuid.UUID, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return {"message": f"Comment with ID {comment_id} removed successfully"}
    raise HTTPException(status_code=404, detail="Comment not found")


@delete_router.delete("/like/{like_id}", status_code=204)
def delete_like(like_id: uuid.UUID, db: Session = Depends(get_db)):
    like = db.query(Like).filter(Like.id == like_id).first()
    if like:
        db.delete(like)
        db.commit()
        return {"message": f"Like with ID {like} removed successfully"}
    raise HTTPException(status_code=404, detail="Like not found")


@delete_router.delete("/follow/{follow_id}", status_code=204)
def delete_follow(follow_id: uuid.UUID, db: Session = Depends(get_db)):
    follow = db.query(Follow).filter(Follow.id == follow_id).first()
    if follow:
        db.delete(follow)
        db.commit()
        return {"message": f"Follow with ID {follow_id} removed successfully"}
    raise HTTPException(status_code=404, detail="Follow not found")
