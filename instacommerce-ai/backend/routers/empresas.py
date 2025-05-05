from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.models import Empresa
from backend.schemas import EmpresaRequest
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/registro")
def registrar_empresa(empresa: EmpresaRequest, db: Session = Depends(get_db)):
    if db.query(Empresa).filter(Empresa.correo == empresa.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    if db.query(Empresa).filter(Empresa.rut == empresa.rut).first():
        raise HTTPException(status_code=400, detail="RUT ya registrado")

    password_hash = pwd_context.hash(empresa.password)

    nueva_empresa = Empresa(
        nombre_empresa=empresa.nombre_empresa,
        rut=empresa.rut,
        correo=empresa.correo,
        tipo_productos=empresa.tipo_productos,
        password_hash=password_hash,
        estado_pago="pendiente"
    )
    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return {"message": "Registro exitoso", "empresa_id": nueva_empresa.id}
