from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from sqlalchemy import or_

auth_router = APIRouter()


@auth_router.post("/signup", status_code=201)
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
        raise HTTPException(
            status_code=400, detail="User with email or mobile number already exits"
        )
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


@auth_router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}"
        )
    user = (
        db.query(User)
        .filter(User.email == data["email"], User.password == data["password"])
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username or password")

    return {"message": "Login successful", "user_id": user.id, "username": user.name}
