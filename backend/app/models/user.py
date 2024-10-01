from pydantic import BaseModel

# Modelo para el registro o uso general de usuarios
class User(BaseModel):
    username: str
    email: str
    password: str
    role: str  # Ejemplo: SuperAdmin, ClientAdmin, etc.

# Modelo para almacenar el hash de la contraseña
class UserInDB(User):
    hashed_password: str

# Modelo exclusivo para login
class UserLogin(BaseModel):
    username: str
    password: str
