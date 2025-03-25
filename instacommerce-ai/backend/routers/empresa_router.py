from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from schemas.schemas import EmpresaRequest, EmpresaResponse

# Importar subrouters
from routers import empresa_register, empresa_login

router = APIRouter(prefix="/empresas", tags=["Empresas"])

# Subrouters (registro y login)
router.include_router(empresa_register.router)
router.include_router(empresa_login.router)

# Listado de empresas
@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()
    return empresas

# Obtener detalle de una empresa
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa
