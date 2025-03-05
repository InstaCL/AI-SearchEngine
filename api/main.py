from fastapi import FastAPI
from agent.chat_interface import interact_with_agent

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenido a AI-SearchEngine API 🚀"}

@app.get("/search")
def search(query: str):
    """
    Endpoint para buscar productos basados en la consulta del usuario.
    """
    response = interact_with_agent(query)
    return {"query": query, "response": response}
