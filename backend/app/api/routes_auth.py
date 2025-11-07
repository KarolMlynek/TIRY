from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.db.session import get_db
from backend.app.db.crud import crud_user
from backend.app.schemas.user import UserCreate, UserOut
from backend.app.core.security import create_access_token

router = APIRouter()

@router.post('/register', response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = crud_user.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = crud_user.create_user(db, email=user_in.email, password=user_in.password, full_name=user_in.full_name)
    return user

@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
