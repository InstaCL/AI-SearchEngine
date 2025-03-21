from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String(255), nullable=False)
    rut = Column(String(100), nullable=False, unique=True)
    correo = Column(String(255), nullable=False, unique=True)
    tipo_productos = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    estado_pago = Column(String(50), default="pendiente")
    api_key_openai = Column(String(255), nullable=True)
    api_key_pinecone = Column(String(255), nullable=True)
    endpoint_productos = Column(Text, nullable=True)
    api_productos_estado = Column(String(50), default="pendiente")
    atributos_sincronizacion = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
