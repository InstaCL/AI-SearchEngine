from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database.database import get_db
from database.models import Empresa
from backend.schemas.schemas import EmpresaCreate, EmpresaResponse

router = APIRouter()

# Contexto de hashing para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/registro", response_model=EmpresaResponse)
def registrar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    existing_email = db.query(Empresa).filter(Empresa.correo == empresa.correo).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")

    existing_rut = db.query(Empresa).filter(Empresa.rut == empresa.rut).first()
    if existing_rut:
        raise HTTPException(status_code=400, detail="⚠️ RUT ya registrado.")

    hashed_password = pwd_context.hash(empresa.password)

    nueva_empresa = Empresa(
        nombre_empresa=empresa.nombre_empresa,
        rut=empresa.rut,
        correo=empresa.correo,
        tipo_productos=empresa.tipo_productos,
        password_hash=hashed_password,
        estado_pago="pendiente"
    )

    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return nueva_empresa