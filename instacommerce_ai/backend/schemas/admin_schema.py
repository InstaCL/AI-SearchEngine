from pydantic import BaseModel, EmailStr

class AdminLoginRequest(BaseModel):
    correo: EmailStr
    password: str

class AdminLoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    admin_id: int
    nombre_admin: str
