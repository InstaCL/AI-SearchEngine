from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from pydantic import BaseModel
from backend.database.database import get_db
from backend.database.models import Chat, ChatMensaje, HistorialConversacion
from backend.agent.subordinate_agent import construir_respuesta_usuario
from backend.agent.leader_agent import validar_respuesta_subordinado

router = APIRouter()

class ChatInput(BaseModel):
    empresa_id: int
    mensaje: str
    chat_id: Optional[str] = None

@router.post("/chat")
def conversar_con_agente(datos: ChatInput, db: Session = Depends(get_db)):
    chat_id = datos.chat_id or str(uuid4())

    # Crear chat si no existe
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        chat = Chat(id=chat_id, empresa_id=datos.empresa_id)
        db.add(chat)
        db.commit()

    # Guardar mensaje del usuario
    mensaje_usuario = ChatMensaje(chat_id=chat_id, contenido=f"Usuario: {datos.mensaje}")
    db.add(mensaje_usuario)
    db.commit()

    # Obtener contexto (solo mensajes del usuario)
    mensajes_previos = db.query(ChatMensaje).filter(ChatMensaje.chat_id == chat_id).order_by(ChatMensaje.id.asc()).all()
    contexto = [m.contenido for m in mensajes_previos if m.contenido.startswith("Usuario:")]

    # Subordinado responde basado en el contexto y la empresa
    respuesta_sub, productos = construir_respuesta_usuario(
        mensaje_usuario=datos.mensaje,
        contexto=contexto,
        empresa_id=datos.empresa_id
    )

    # Líder analiza y mejora la respuesta del subordinado
    respuesta_lider = validar_respuesta_subordinado(
        respuesta_subordinado=respuesta_sub,
        contexto=contexto,
        mensaje_usuario=datos.mensaje,
        productos=productos
    )

    # Guardar respuestas del agente
    db.add_all([
        ChatMensaje(chat_id=chat_id, contenido=respuesta_sub),
        ChatMensaje(chat_id=chat_id, contenido=respuesta_lider)
    ])
    db.commit()

    # 🧠 Crear resumen y guardar historial
    resumen_conversacion = f"📝 Resumen: El cliente preguntó: '{datos.mensaje}'. El agente sugirió productos relacionados y ofreció asistencia adicional."
    productos_mencionados = ", ".join([p["title"] for p in productos]) if productos else "Ninguno"
    resumen = f"📝 Resumen: El cliente preguntó: '{datos.mensaje}'. El agente sugirió productos relacionados y ofreció asistencia adicional."


    historial = HistorialConversacion(
        empresa_id=datos.empresa_id,
        chat_id=chat_id,
        resumen=resumen,
        productos_mencionados=productos_mencionados
    )
    db.add(historial)
    db.commit()

    # Últimos 3 mensajes
    ultimos = db.query(ChatMensaje).filter(ChatMensaje.chat_id == chat_id).order_by(ChatMensaje.id.desc()).limit(3).all()

    return {
        "chat_id": chat_id,
        "conversacion": [m.contenido for m in reversed(ultimos)]
    }

@router.get("/chat/{chat_id}")
def obtener_conversacion(chat_id: str, db: Session = Depends(get_db)):
    mensajes = db.query(ChatMensaje).filter(ChatMensaje.chat_id == chat_id).order_by(ChatMensaje.id.asc()).all()

    if not mensajes:
        raise HTTPException(status_code=404, detail="❌ No se encontraron mensajes para este chat_id")

    conversacion = [mensaje.contenido for mensaje in mensajes]
    return {
        "chat_id": chat_id,
        "conversacion": conversacion
    }
