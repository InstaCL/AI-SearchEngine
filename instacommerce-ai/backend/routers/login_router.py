from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.database.database import get_db
from backend.database.models import Empresa
from backend.schemas.schemas import EmpresaLoginRequest, EmpresaLoginResponse

router = APIRouter()

# Configuración de hasheo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=EmpresaLoginResponse)
def login_empresa(data: EmpresaLoginRequest, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.correo == data.correo).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no registrada.")
    if not pwd_context.verify(data.password, empresa.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta.")
    if empresa.estado_pago != "aprobado":
        raise HTTPException(status_code=403, detail="⚠️ Acceso denegado: pago pendiente.")

    return EmpresaLoginResponse(
        message=f"✅ Bienvenido {empresa.nombre_empresa}",
        empresa_id=empresa.id,
        tipo_productos=empresa.tipo_productos
    )