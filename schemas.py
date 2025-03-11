from pydantic import BaseModel

class EmpresaRequest(BaseModel):
    nombre_empresa: str
    rut: str
    correo: str
    tipo_productos: str
    password: str

class CredencialesUpdate(BaseModel):
    api_key_openai: str
    api_key_pinecone: str
    endpoint_productos: str
