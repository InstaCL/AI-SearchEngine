# agent/subordinate_agent.py (actualizado)

from database.database import get_db
from database.models import ChatMensaje
from typing import List, Tuple
from agent.leader_agent import validar_respuesta_subordinado
from pinecone_module.pinecone_manager import buscar_productos_relacionados

def construir_respuesta_usuario(mensaje_usuario: str, contexto: List[str], empresa_id: int) -> Tuple[str, List[dict]]:
    productos = buscar_productos_relacionados(mensaje_usuario, empresa_id)

    if not productos:
        return "(Subordinado): No encontré productos relacionados en este momento.", []

    productos_texto = "\n".join(
        f"🔹 Producto {i+1}:\n📌 *{producto['title']}*\n💲 Precio: ${producto['price']}\n📝 {producto.get('description', '')}"
        for i, producto in enumerate(productos)
    )

    respuesta = f"(Subordinado): Aquí tienes algunos productos recomendados:\n\n{productos_texto}"
    return respuesta, productos

