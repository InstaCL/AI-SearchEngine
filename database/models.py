from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, nullable=False)
    rut = Column(String, nullable=False, unique=True)
    correo = Column(String, unique=True, nullable=False)
    tipo_productos = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    estado_pago = Column(String, default="pendiente")
    api_productos_estado = Column(String, default="pendiente")  # nuevo campo
    endpoint_productos = Column(Text, nullable=True)
    api_key_openai = Column(Text, nullable=True)
    api_key_pinecone = Column(Text, nullable=True)
    atributos_sincronizacion = Column(Text, nullable=True)  # se guardará JSON serializado
    fecha_registro = Column(DateTime, default=datetime.utcnow)