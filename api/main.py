from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.chat_interface import interact_with_agent
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
