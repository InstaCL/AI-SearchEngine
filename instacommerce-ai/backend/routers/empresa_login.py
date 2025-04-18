from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.empresa_schema import EmpresaLoginRequest
from database.models import Empresa
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from config import settings
from routers.auth_utils import obtener_empresa_actual  # ✅

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login_empresa(request: EmpresaLoginRequest, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.correo == request.correo).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no registrada.")
    if not pwd_context.verify(request.password, empresa.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta.")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "empresa_id": empresa.id,
        "exp": expire
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "empresa_id": empresa.id,
        "nombre_empresa": empresa.nombre_empresa,
        "estado_pago": empresa.estado_pago,
        "tipo_productos": empresa.tipo_productos
    }

# ✅ NUEVO ENDPOINT /empresa/perfil protegido por JWT
@router.get("/perfil")
def perfil_empresa(empresa: Empresa = Depends(obtener_empresa_actual)):
    return {
        "id": empresa.id,
        "nombre_empresa": empresa.nombre_empresa,
        "correo": empresa.correo,
        "rut": empresa.rut,
        "tipo_productos": empresa.tipo_productos,
        "estado_pago": empresa.estado_pago,
    }
