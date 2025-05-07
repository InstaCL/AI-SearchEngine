from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from database.database import get_db
from config.settings import settings
from backend.schemas.admin_schema import AdminLoginRequest, AdminLoginResponse
from database.models import Empresa  # Se utiliza Empresa como modelo de admin predefinido

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

router = APIRouter(tags=["Admin Login"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=AdminLoginResponse)
def login_admin(request: AdminLoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Empresa).filter(Empresa.correo == request.correo).first()

    if not admin:
        raise HTTPException(status_code=404, detail="❌ Admin no registrado.")
    if admin.correo != "christopher.lara@instacommerce.cl":
        raise HTTPException(status_code=403, detail="⛔ Solo acceso administrador permitido.")
    if not pwd_context.verify(request.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta.")

    payload = {
        "admin_id": admin.id,
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return AdminLoginResponse(
        access_token=token,
        token_type="bearer",
        admin_id=admin.id,
        nombre_admin=admin.nombre_empresa,
        message="✅ Acceso concedido como administrador"
    )
