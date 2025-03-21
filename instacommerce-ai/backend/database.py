from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Ruta de la base de datos SQLite (puede cambiarse por PostgreSQL en producción)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Crear motor y sesión
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()

# Dependency para inyección de sesiones

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
