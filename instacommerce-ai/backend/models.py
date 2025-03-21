from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String(255), nullable=False)
    rut = Column(String(50), unique=True, nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    tipo_productos = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    estado_pago = Column(String(50), default="pendiente")

    api_key_openai = Column(String(255), nullable=True)
    api_key_pinecone = Column(String(255), nullable=True)
    endpoint_productos = Column(String(500), nullable=True)
    api_productos_estado = Column(String(50), default="pendiente")
    atributos_sincronizacion = Column(Text, nullable=True)

    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())