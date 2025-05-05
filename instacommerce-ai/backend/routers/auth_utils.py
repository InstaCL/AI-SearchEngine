from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.models import Empresa
from backend.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# ✅ Usamos HTTPBearer en lugar de OAuth2PasswordBearer
oauth2_scheme = HTTPBearer()

def obtener_empresa_actual(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Empresa:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        empresa_id: int = payload.get("empresa_id")
        if not empresa_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="⛔ Token inválido o no autorizado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="⛔ Token inválido o no autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    return empresa
