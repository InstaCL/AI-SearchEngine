from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from agent.chat_interface import interact_with_agent
from database.database import get_db
from database.models import Cliente, Base
import traceback

app = FastAPI()

# 🔥 SOLUCIÓN: Habilitar CORS para permitir conexiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite solicitudes desde React
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
def home():
    return {"message": "Bienvenido a AI-SearchEngine API 🚀"}

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

# 📌 NUEVO: Endpoints para manejar clientes

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
