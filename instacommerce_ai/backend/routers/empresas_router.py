from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from backend.schemas.schemas import EmpresaRequest, EmpresaResponse, CredencialesUpdate  # ✅ Importación extra

# Importar subrouters
from backend.routers import empresa_register, empresa_login

router = APIRouter(prefix="/empresas", tags=["Empresas"])

# Subrouters (registro y login)
router.include_router(empresa_register.router)
router.include_router(empresa_login.router)

# Listado de empresas
@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    print("📡 Endpoint /empresas/ accedido")
    empresas = db.query(Empresa).all()
    return empresas

# Obtener detalle de una empresa
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

# ✅ Actualización técnica (incluye índice Pinecone)
@router.put("/{empresa_id}")
def actualizar_empresa(empresa_id: int, datos: CredencialesUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    if datos.api_key_openai is not None:
        empresa.api_key_openai = datos.api_key_openai
    if datos.api_key_pinecone is not None:
        empresa.api_key_pinecone = datos.api_key_pinecone
    if datos.endpoint_productos is not None:
        empresa.endpoint_productos = datos.endpoint_productos
    if hasattr(datos, "indice_pinecone") and datos.indice_pinecone is not None:
        empresa.indice_pinecone = datos.indice_pinecone  # ✅ nuevo campo

    db.commit()
    return {"message": "✅ Empresa actualizada correctamente"}

# Prueba de funcionamiento
@router.get("/ping")
def ping_empresas():
    print("✅ Router empresas funciona")
    return {"mensaje": "pong desde empresas"}
