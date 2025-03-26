# agent/subordinate_agent.py (actualizado)

from database.database import get_db
from database.models import ChatMensaje
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.orm import Session
from agent.leader_agent import validar_respuesta_subordinado
from pinecone_module.pinecone_manager import buscar_productos_relacionados

def construir_respuesta_usuario(mensaje_usuario: str, contexto: list, empresa_id: int) -> str:
    productos = buscar_productos_relacionados(mensaje_usuario, empresa_id)
    
    if not productos:
        return "(Subordinado): No encontré productos relacionados en este momento."
    
    productos_texto = "\n".join(
        f"- {producto['title']} (${producto['price']})" for producto in productos
    )

    return f"(Subordinado): Basado en tu mensaje, aquí hay algunas opciones:\n{productos_texto}"
