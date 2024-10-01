from fastapi import APIRouter, HTTPException
from app.models.user import User, UserInDB
from app.db import users_collection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_router = APIRouter()

# Endpoint para registrar usuarios
@users_router.post("/register")
async def create_user(user: User):
    # Verifica si el usuario ya existe
    db_user = users_collection.find_one({"username": user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Hash de la contraseña
    hashed_password = pwd_context.hash(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)

    # Insertar usuario en la base de datos
    users_collection.insert_one(user_in_db.dict())
    return {"message": "Usuario creado exitosamente"}

# Endpoint para obtener el perfil del usuario
@users_router.get("/me")
async def get_user_profile(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
