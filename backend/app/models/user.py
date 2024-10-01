from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    role: str  # SuperAdmin, ClientAdmin, ClientDeveloper, ClientViewer
