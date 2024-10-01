import bcrypt
from pymongo import MongoClient
from decouple import config

# Conexión a MongoDB
client = MongoClient(config("MONGO_URI"))
db = client["bi"]  # Nombre de tu base de datos
users_collection = db["users"]

# Función para crear usuarios
def create_user(username, email, password, role):
    # Generar el hash de la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Crear el documento de usuario
    user = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password.decode('utf-8'),
        "role": role
    }

    # Insertar el usuario en la base de datos
    result = users_collection.insert_one(user)
    print(f"Usuario {username} creado con el ID: {result.inserted_id}")

# Ejemplo de uso: agregar varios usuarios
if __name__ == "__main__":
    # Crea el usuario admin
    create_user("admin", "admin@example.com", "admin123", "SuperAdmin")

    # Crea otro usuario
    create_user("user1", "user1@example.com", "password123", "ClientAdmin")
