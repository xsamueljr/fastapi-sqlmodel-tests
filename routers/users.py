from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from db.models.user import UserCreate, UserRead, UserLogin, User
from dependencies import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=201, response_model=UserRead)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    # Create a new user
    new_user = User.model_validate(user)
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        error = str(e)
        if "user.username" in error:
            raise HTTPException(status_code=409, detail="Username already exists")
        
        if "user.email" in error:
            raise HTTPException(status_code=409, detail="Email already exists")

    return new_user


@router.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    statement = select(User).where(
        User.username == user_login.username,
        User.password == user_login.password
    )
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Login successful"}