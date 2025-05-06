from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import os

# 🔁 Cambiar a db.sqlite3
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"  # O PostgreSQL/Mysql

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
    pool_size=20,
    max_overflow=30,
    pool_timeout=60,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tablas al ejecutar
def init_db():
    print("✅ Creando base de datos y tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente!")
