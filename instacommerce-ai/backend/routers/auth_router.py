from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.database import get_db
from database.models import Empresa
from schemas import LoginRequest, LoginResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=LoginResponse)
def login_empresa(credentials: LoginRequest, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.correo == credentials.correo).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no registrada.")

    if not pwd_context.verify(credentials.password, empresa.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta.")

    if empresa.estado_pago != "aprobado":
        raise HTTPException(status_code=403, detail="⚠️ Acceso denegado: pago pendiente.")

    return LoginResponse(
        message=f"✅ Bienvenido {empresa.nombre_empresa}",
        empresa_id=empresa.id,
        tipo_productos=empresa.tipo_productos
    )
