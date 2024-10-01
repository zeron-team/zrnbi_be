from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import auth_router
from app.routes.users import users_router

app = FastAPI()

# Middleware para habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://31.220.76.74:3000"],  # React localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")

@app.get("/")
async def root():
    return {"message": "Bienvenido al backend de BI SaaS"}
