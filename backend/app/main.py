from fastapi import FastAPI
from app.routes import auth  # Ajusta esta línea según tu estructura de rutas

app = FastAPI()

# Incluye el router de autenticación (o cualquier otro que tengas)
app.include_router(auth.auth_router)

# Verifica que tu aplicación esté configurada correctamente
