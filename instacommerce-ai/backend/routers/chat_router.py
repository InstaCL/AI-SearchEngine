from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from pydantic import BaseModel
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import Chat, ChatMensaje
from agent.subordinate_agent import construir_respuesta_usuario

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

    # Respuestas simuladas
    respuesta_sub = f"(Subordinado): Encontré un producto basado en lo que dijiste: '{datos.mensaje}'"
    respuesta_lider = "(Líder): Revisé la info del subordinado y me parece adecuada."

    # Guardar mensajes en la base de datos
    mensajes = [
        ChatMensaje(chat_id=chat_id, contenido=f"Usuario: {datos.mensaje}"),
        ChatMensaje(chat_id=chat_id, contenido=respuesta_sub),
        ChatMensaje(chat_id=chat_id, contenido=respuesta_lider),
    ]
    db.add_all(mensajes)
    db.commit()

    # Recuperar últimos 3 mensajes
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
