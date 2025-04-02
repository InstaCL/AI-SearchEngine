from pydantic import BaseModel

class LoginEmpresa(BaseModel):
    usuario: str
    password: str
