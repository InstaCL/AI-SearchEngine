from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from pydantic import BaseModel
from database.database import get_db
from database.models import Chat, ChatMensaje, Empresa
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

    # Validar que la empresa tenga credenciales técnicas completas
    empresa = db.query(Empresa).filter(Empresa.id == datos.empresa_id).first()
    if not empresa or not all([empresa.api_key_openai, empresa.api_key_pinecone, empresa.endpoint_productos]):
        raise HTTPException(
            status_code=403,
            detail="❌ Esta empresa no tiene sus credenciales técnicas configuradas. Contacta al administrador."
        )

    # Crear chat si no existe
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        chat = Chat(id=chat_id, empresa_id=datos.empresa_id)
        db.add(chat)
        db.commit()

    # Guardar mensaje del usuario
    mensaje_usuario = f"Usuario: {datos.mensaje}"
    db.add(ChatMensaje(chat_id=chat_id, contenido=mensaje_usuario))
    db.commit()

    # Obtener contexto anterior
    mensajes_previos = db.query(ChatMensaje).filter(ChatMensaje.chat_id == chat_id).order_by(ChatMensaje.id).all()
    contexto = [m.contenido for m in mensajes_previos]

    # Agente subordinado genera respuesta
    respuesta_sub = construir_respuesta_usuario(datos.mensaje, contexto, datos.empresa_id)

    # Agente líder valida respuesta
    respuesta_lider = validar_respuesta_subordinado(respuesta_sub, contexto, datos.mensaje)

    # Guardar respuestas
    db.add_all([
        ChatMensaje(chat_id=chat_id, contenido=respuesta_sub),
        ChatMensaje(chat_id=chat_id, contenido=respuesta_lider),
    ])
    db.commit()

    return {
        "chat_id": chat_id,
        "conversacion": [mensaje_usuario, respuesta_sub, respuesta_lider]
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
