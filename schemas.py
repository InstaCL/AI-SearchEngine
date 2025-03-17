# schemas.py

from pydantic import BaseModel

# 📦 Esquema para el registro de empresa
class EmpresaRequest(BaseModel):
    nombre_empresa: str
    rut: str
    correo: str
    tipo_productos: str
    password: str

# 🔐 Esquema para actualizar credenciales técnicas (API Keys y endpoint)
class CredencialesUpdate(BaseModel):
    api_key_openai: str
    api_key_pinecone: str
    endpoint_productos: str

# Nuevo esquema EndpointProductosUpdate
class EndpointProductosUpdate(BaseModel):
    endpoint_productos: str
