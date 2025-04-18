from pydantic import BaseModel, EmailStr

class EmpresaRegisterRequest(BaseModel):
    nombre_empresa: str
    rut: str
    correo: EmailStr
    tipo_productos: str
    password: str

class EmpresaLoginRequest(BaseModel):
    correo: EmailStr
    password: str
