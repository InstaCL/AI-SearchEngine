from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schemas import EmpresaRequest, EmpresaResponse
from schemas.schemas import EmpresaRegisterRequest
from database.models import Empresa
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/empresas/registro")
def registrar_empresa(request: EmpresaRegisterRequest, db: Session = Depends(get_db)):
    if db.query(Empresa).filter(Empresa.correo == request.correo).first():
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")
    if db.query(Empresa).filter(Empresa.rut == request.rut).first():
        raise HTTPException(status_code=400, detail="⚠️ RUT ya registrado.")

    password_hash = pwd_context.hash(request.password)

    nueva_empresa = Empresa(
        nombre_empresa=request.nombre_empresa,
        rut=request.rut,
        correo=request.correo,
        tipo_productos=request.tipo_productos,
        password_hash=password_hash,
        estado_pago="pendiente"
    )

    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return {"message": "✅ Empresa registrada exitosamente", "empresa_id": nueva_empresa.id}
