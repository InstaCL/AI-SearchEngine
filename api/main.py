from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from agent.chat_interface import interact_with_agent
from database.database import get_db
from database.models import Empresa, Base
from schemas import EmpresaRequest, CredencialesUpdate
from passlib.context import CryptContext
from client.fetch_products import fetch_products
from pinecone_module.pinecone_manager import insert_product
from fastapi import Path
import traceback

app = FastAPI()

# 🔐 Contexto para hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔥 CORS para conexión con React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🏠 Endpoint raíz
@app.get("/")
def home():
    return {"message": "Bienvenido a AI-SearchEngine API 🚀"}

# 🔍 Búsqueda de productos
@app.get("/search")
def search(query: str, empresa_id: int, db: Session = Depends(get_db)):
    try:
        response = interact_with_agent(query, empresa_id=empresa_id)
        return {"query": query, "response": response}
    except Exception as e:
        print("❌ ERROR EN LA API:")
        traceback.print_exc()
        return {"error": "Ocurrió un error en el servidor", "details": str(e)}

# 🏢 Registro de Empresa
@app.post("/registro")
def registrar_empresa(empresa: EmpresaRequest, db: Session = Depends(get_db)):
    if db.query(Empresa).filter(Empresa.correo == empresa.correo).first():
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")
    if db.query(Empresa).filter(Empresa.rut == empresa.rut).first():
        raise HTTPException(status_code=400, detail="⚠️ RUT ya registrado.")

    password_hash = pwd_context.hash(empresa.password)

    nueva_empresa = Empresa(
        nombre_empresa=empresa.nombre_empresa,
        rut=empresa.rut,
        correo=empresa.correo,
        tipo_productos=empresa.tipo_productos,
        password_hash=password_hash,
        estado_pago="aprobado"  # Simulación de pago exitoso
    )

    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return {
        "message": "✅ Registro exitoso. Acceso habilitado.",
        "empresa_id": nueva_empresa.id
    }

# 🔐 Login de Empresa
@app.post("/login")
def login_empresa(correo: str, password: str, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.correo == correo).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no registrada.")
    if not pwd_context.verify(password, empresa.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta.")
    if empresa.estado_pago != "aprobado":
        raise HTTPException(status_code=403, detail="⚠️ Acceso denegado: pago pendiente.")

    return {
        "message": f"✅ Bienvenido {empresa.nombre_empresa}",
        "empresa_id": empresa.id,
        "tipo_productos": empresa.tipo_productos
    }

# 🔄 Sincronización de productos
@app.post("/sync-empresa-productos")
def sync_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    productos = fetch_products()

    for producto in productos:
        insert_product(
            product_id=producto["id"],
            product_name=producto["title"],
            description=producto["description"],
            empresa_id=empresa_id
        )

    return {
        "message": f"✅ Productos sincronizados correctamente para {empresa.nombre_empresa}",
        "total": len(productos)
    }

# 🔐 Actualizar credenciales API Keys y endpoint
@app.put("/empresa/{empresa_id}/credenciales")
def actualizar_credenciales(
    empresa_id: int = Path(..., description="ID de la empresa"),
    credenciales: CredencialesUpdate = Depends(),
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    empresa.api_key_openai = credenciales.api_key_openai
    empresa.api_key_pinecone = credenciales.api_key_pinecone
    empresa.endpoint_productos = credenciales.endpoint_productos

    db.commit()
    db.refresh(empresa)

    return {
        "message": "✅ Credenciales actualizadas correctamente",
        "empresa_id": empresa.id
    }

# 📋 Obtener lista de empresas registradas
@app.get("/empresas")
def obtener_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()
    return empresas


@app.put("/empresas/{empresa_id}/configuracion")
def actualizar_configuracion_tecnica(
    empresa_id: int = Path(..., description="ID de la empresa"),
    api_key_openai: str = "",
    api_key_pinecone: str = "",
    endpoint_productos: str = "",
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    empresa.api_key_openai = api_key_openai
    empresa.api_key_pinecone = api_key_pinecone
    empresa.endpoint_productos = endpoint_productos

    db.commit()
    db.refresh(empresa)

    return {
        "message": "✅ Configuración técnica actualizada correctamente",
        "empresa_id": empresa.id
    }