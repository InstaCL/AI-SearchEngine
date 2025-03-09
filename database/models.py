from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    endpoint_productos = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, nullable=False)
    rut = Column(String, nullable=False, unique=True)
    correo = Column(String, unique=True, nullable=False)
    tipo_productos = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    estado_pago = Column(String, default="aprobado")  # Simulación por ahora
    fecha_registro = Column(DateTime, default=datetime.utcnow)