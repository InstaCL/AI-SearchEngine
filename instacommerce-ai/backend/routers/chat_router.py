from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from pydantic import BaseModel
from database.database import get_db
from database.models import Chat, ChatMensaje
from agent.subordinate_agent import construir_respuesta_usuario
from agent.leader_agent import validar_respuesta_subordinado

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

    # Obtener contexto del chat (mensajes anteriores)
    mensajes_previos = db.query(ChatMensaje).filter(ChatMensaje.chat_id == chat_id).order_by(ChatMensaje.id).all()
    contexto = [m.contenido for m in mensajes_previos]

    # Agente subordinado genera respuesta basada en productos reales
    respuesta_sub = construir_respuesta_usuario(datos.mensaje, contexto, datos.empresa_id)

    # Agente líder valida la respuesta del subordinado
    respuesta_lider = validar_respuesta_subordinado(respuesta_sub, contexto, datos.mensaje)

    # Guardar nuevo turno de conversación
    mensajes = [
        ChatMensaje(chat_id=chat_id, contenido=f"Usuario: {datos.mensaje}"),
        ChatMensaje(chat_id=chat_id, contenido=respuesta_sub),
        ChatMensaje(chat_id=chat_id, contenido=respuesta_lider),
    ]
    db.add_all(mensajes)
    db.commit()

    # Obtener últimos 3 mensajes de este turno
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
