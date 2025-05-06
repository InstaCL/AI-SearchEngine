from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from database.database import get_db
from database.models import Empresa
from config.settings import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="empresa/login")

@router.get("/empresa/perfil")
def obtener_perfil_empresa(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        empresa_id = payload.get("empresa_id")
        if not empresa_id:
            raise HTTPException(status_code=401, detail="Token inválido")

        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")

        return {
            "id": empresa.id,
            "nombre_empresa": empresa.nombre_empresa,
            "correo": empresa.correo,
            "rut": empresa.rut,
            "giro": empresa.tipo_productos,
            "estado_pago": empresa.estado_pago
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
