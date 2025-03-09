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
