from sqlalchemy import Column, Integer, String, DateTime
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
    estado_pago = Column(String, default="pendiente")  # por defecto pendiente, se actualizará a "aprobado" luego del pago
    api_key_openai = Column(String, nullable=True)
    api_key_pinecone = Column(String, nullable=True)
    endpoint_productos = Column(String, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)