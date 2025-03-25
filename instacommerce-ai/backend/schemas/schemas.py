from pydantic import BaseModel, EmailStr
from typing import Optional, List

class EmpresaRequest(BaseModel):
    nombre_empresa: str
    rut: str
    correo: EmailStr
    tipo_productos: str
    password: str

class EmpresaResponse(BaseModel):
    id: int
    nombre_empresa: str
    rut: str
    correo: EmailStr
    tipo_productos: str
    estado_pago: str

    class Config:
        from_attributes = True

class EmpresaRegisterRequest(BaseModel):
    nombre_empresa: str
    rut: str
    correo: EmailStr
    tipo_productos: str
    password: str 

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    empresa_id: int
    tipo_productos: str

class CredencialesUpdate(BaseModel):
    api_key_openai: Optional[str] = None
    api_key_pinecone: Optional[str] = None
    endpoint_productos: Optional[str] = None

class EndpointProductosUpdate(BaseModel):
    endpoint_productos: str

class AtributosSeleccionUpdate(BaseModel):
    atributos: List[str]
