from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.models import Empresa
from pydantic import BaseModel, EmailStr, constr
from passlib.hash import bcrypt
import re

router = APIRouter()

# ---------------------------
# MODELO DE REGISTRO
# ---------------------------
class EmpresaRegistroRequest(BaseModel):
    nombre_empresa: str
    correo: EmailStr
    rut: str
    rubro: str
    password: constr(min_length=8)
    recaptcha_token: str  # Puedes usarlo si más adelante validas con Google reCAPTCHA

# ---------------------------
# ENDPOINT DE REGISTRO
# ---------------------------
@router.post("/registro")
def registrar_empresa(data: EmpresaRegistroRequest, db: Session = Depends(get_db)):
    # Validar RUT
    if not re.match(r"^\d{6,9}-[\dkK]$", data.rut):
        raise HTTPException(status_code=400, detail="❌ Formato de RUT inválido. Debe ser tipo 12345678-9")

    # Validar unicidad de correo
    if db.query(Empresa).filter(Empresa.correo == data.correo).first():
        raise HTTPException(status_code=400, detail="❌ Ya existe una empresa registrada con este correo")

    # Validar unicidad de RUT
    if db.query(Empresa).filter(Empresa.rut == data.rut).first():
        raise HTTPException(status_code=400, detail="❌ Ya existe una empresa registrada con este RUT")

    # Crear nueva empresa
    nueva_empresa = Empresa(
        nombre_empresa=data.nombre_empresa,
        correo=data.correo,
        rut=data.rut,
        tipo_productos=data.rubro,
        password_hash=bcrypt.hash(data.password),
        estado_pago="pendiente"
    )

    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return {
        "message": "✅ Empresa registrada correctamente",
        "empresa_id": nueva_empresa.id,
        "nombre_empresa": nueva_empresa.nombre_empresa
    }
