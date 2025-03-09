from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from agent.chat_interface import interact_with_agent
from database.database import get_db
from database.models import Cliente, Empresa, Base
from passlib.context import CryptContext
import traceback

app = FastAPI()

# 🔐 Contexto para hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔥 Habilitar CORS para conexión con React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde React
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
def search(query: str):
    """
    Endpoint para buscar productos basados en la consulta del usuario.
    """
    try:
        response = interact_with_agent(query)
        return {"query": query, "response": response}
    except Exception as e:
        print("❌ ERROR EN LA API:")
        traceback.print_exc()
        return {"error": "Ocurrió un error en el servidor", "details": str(e)}

# 🛠 Endpoints para manejar clientes
@app.post("/clientes")
def crear_cliente(nombre: str, api_key: str, endpoint_productos: str, db: Session = Depends(get_db)):
    """
    Crea un nuevo cliente en la base de datos.
    """
    nuevo_cliente = Cliente(nombre=nombre, api_key=api_key, endpoint_productos=endpoint_productos)
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return {"message": "✅ Cliente creado correctamente", "id": nuevo_cliente.id}

@app.get("/clientes")
def obtener_clientes(db: Session = Depends(get_db)):
    """
    Retorna la lista de clientes registrados.
    """
    clientes = db.query(Cliente).all()
    return clientes

# 🏢 Registro de Empresas
@app.post("/registro")
def registrar_empresa(
    nombre_empresa: str,
    rut: str,
    correo: str,
    tipo_productos: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    Registra una nueva empresa con contraseña encriptada.
    Simula que el estado de pago está aprobado.
    """
    # Verificar duplicados
    if db.query(Empresa).filter(Empresa.correo == correo).first():
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")
    if db.query(Empresa).filter(Empresa.rut == rut).first():
        raise HTTPException(status_code=400, detail="⚠️ RUT ya registrado.")

    # Hashear la contraseña
    password_hash = pwd_context.hash(password)

    nueva_empresa = Empresa(
        nombre_empresa=nombre_empresa,
        rut=rut,
        correo=correo,
        tipo_productos=tipo_productos,
        password_hash=password_hash,
        estado_pago="aprobado"  # Simulación del pago exitoso
    )

    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    return {
        "message": "✅ Registro exitoso. Acceso habilitado.",
        "empresa_id": nueva_empresa.id
    }
