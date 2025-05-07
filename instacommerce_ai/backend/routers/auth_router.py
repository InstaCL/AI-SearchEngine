from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.database import get_db
from database.models import Empresa
from backend.schemas.login_empresa import LoginEmpresa

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login_empresa(datos: LoginEmpresa, db: Session = Depends(get_db)):
    # Buscar empresa por correo o alias
    empresa = db.query(Empresa).filter(
        (Empresa.correo == datos.usuario) | (Empresa.nombre_empresa == datos.usuario)
    ).first()

    if not empresa:
        raise HTTPException(status_code=401, detail="❌ Usuario no encontrado")

    if not pwd_context.verify(datos.password, empresa.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta")

    return {
        "mensaje": "✅ Login exitoso",
        "empresa_id": empresa.id,
        "nombre": empresa.nombre_empresa
    }
