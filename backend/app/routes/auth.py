from fastapi import APIRouter, HTTPException
from app.models.user import UserLogin  # Importar el nuevo modelo de login
from app.db import users_collection
from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime
from decouple import config

# Cargar las variables desde el archivo .env
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()

# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint para el inicio de sesión
@auth_router.post("/login")
async def login(user: UserLogin):  # Usa el nuevo modelo UserLogin
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
