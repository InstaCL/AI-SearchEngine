from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from database.database import Base

class HistorialConversacion(Base):
    __tablename__ = "historial_conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    resumen = Column(Text)
    productos_mencionados = Column(JSON)
    cantidad_mensajes = Column(Integer)
    fecha = Column(DateTime(timezone=True), server_default=func.now())