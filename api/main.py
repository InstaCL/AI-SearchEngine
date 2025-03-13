# api/main.py

from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from agent.chat_interface import interact_with_agent
from database.database import get_db
from database.models import Empresa
from schemas import EmpresaRequest, CredencialesUpdate
from passlib.context import CryptContext
from client.fetch_products import fetch_products
from pinecone_module.pinecone_manager import insert_or_update_product, delete_all_products_by_empresa_id
import traceback

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Bienvenido a AI-SearchEngine API 🚀"}

@app.get("/search")
def search(query: str, empresa_id: int, db: Session = Depends(get_db)):
    try:
        response = interact_with_agent(query, empresa_id=empresa_id)
        return {"query": query, "response": response}
    except Exception as e:
        print("❌ ERROR EN LA API:")
        traceback.print_exc()
        return {"error": "Ocurrió un error en el servidor", "details": str(e)}

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
        estado_pago="aprobado"
    )

    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return {"message": "✅ Registro exitoso", "empresa_id": nueva_empresa.id}

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

@app.post("/sync-empresa-productos")
def sync_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    productos = fetch_products()
    if not productos:
        return {"message": "⚠️ No se encontraron productos para sincronizar"}

    for producto in productos:
        insert_or_update_product(
            product_id=producto["id"],
            product_name=producto["title"],
            description=producto["description"],
            slug=producto["slug"],
            price=producto["price"],
            category_name=producto["category"]["name"],
            category_slug=producto["category"]["slug"],
            image=producto["images"][0] if producto["images"] else "",
            empresa_id=empresa_id
        )

    return {"message": "✅ Productos sincronizados correctamente", "total": len(productos)}

@app.put("/empresas/{empresa_id}/configuracion")
def actualizar_configuracion_tecnica(empresa_id: int, config: CredencialesUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    empresa.api_key_openai = config.api_key_openai
    empresa.api_key_pinecone = config.api_key_pinecone
    empresa.endpoint_productos = config.endpoint_productos

    db.commit()
    db.refresh(empresa)

    return {"message": "✅ Configuración técnica actualizada", "empresa_id": empresa.id}

@app.get("/empresas/{empresa_id}")
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return {
        "id": empresa.id,
        "nombre_empresa": empresa.nombre_empresa,
        "rut": empresa.rut,
        "correo": empresa.correo,
        "tipo_productos": empresa.tipo_productos,
        "estado_pago": empresa.estado_pago,
        "api_key_openai": empresa.api_key_openai,
        "api_key_pinecone": empresa.api_key_pinecone,
        "endpoint_productos": empresa.endpoint_productos,
        "fecha_registro": empresa.fecha_registro
    }

@app.get("/empresas")
def obtener_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@app.delete("/empresas/{empresa_id}/eliminar-productos")
def eliminar_productos_empresa(empresa_id: int):
    return delete_all_products_by_empresa_id(empresa_id)
