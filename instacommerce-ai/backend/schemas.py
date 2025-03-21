from pydantic import BaseModel, EmailStr
from typing import Optional, List

class EmpresaRequest(BaseModel):
    nombre_empresa: str
    rut: str
    correo: EmailStr
    tipo_productos: str
    password: str

class CredencialesUpdate(BaseModel):
    api_key_openai: Optional[str] = None
    api_key_pinecone: Optional[str] = None
    endpoint_productos: Optional[str] = None

class EndpointProductosUpdate(BaseModel):
    endpoint_productos: str

class AtributosSincronizacionUpdate(BaseModel):
    atributos: List[str]

