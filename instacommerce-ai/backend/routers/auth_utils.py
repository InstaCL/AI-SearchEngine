from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="empresa/login")

def obtener_empresa_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Empresa:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        empresa_id: int = payload.get("empresa_id")
        if empresa_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if empresa is None:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        return empresa
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
