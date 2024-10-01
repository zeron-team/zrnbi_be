from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.models.user import User
from app.db import users_collection
from decouple import config
from datetime import datetime, timedelta

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cargar el SECRET_KEY y ALGORITHM desde el archivo .env
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@auth_router.post("/login")
async def login(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Aquí generarías el JWT y lo devolverías


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_router.post("/login")
async def login(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Generar el JWT token y devolverlo
    access_token = create_access_token(data={"sub": db_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}