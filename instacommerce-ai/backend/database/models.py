from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
import json

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String(255), nullable=False)
    rut = Column(String(50), nullable=False, unique=True)
    correo = Column(String(255), nullable=False, unique=True)
    tipo_productos = Column(String(255), nullable=False)  # Rubro o giro
    password_hash = Column(String(255), nullable=False)
    estado_pago = Column(String(50), default="pendiente")
    api_key_openai = Column(Text, nullable=True)
    api_key_pinecone = Column(Text, nullable=True)
    endpoint_productos = Column(Text, nullable=True)
    api_productos_estado = Column(String(50), default="pendiente")
    atributos_sincronizacion = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    indice_pinecone = Column(String, nullable=True)

    def get_atributos_sincronizados(self):
        try:
            return json.loads(self.atributos_sincronizacion or "[]")
        except json.JSONDecodeError:
            return []

    def set_atributos_sincronizados(self, atributos: list[str]):
        self.atributos_sincronizacion = json.dumps(atributos)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(String, primary_key=True, index=True)  # chat_id tipo UUID
    empresa_id = Column(Integer, nullable=False)
    mensajes = relationship("ChatMensaje", back_populates="chat")


class ChatMensaje(Base):
    __tablename__ = "chat_mensajes"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey("chats.id"))
    contenido = Column(String, nullable=False)
    chat = relationship("Chat", back_populates="mensajes")


class HistorialConversacion(Base):
    __tablename__ = "historial_conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, nullable=False)
    chat_id = Column(String, nullable=False)
    resumen = Column(Text, nullable=False)
    productos_mencionados = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
