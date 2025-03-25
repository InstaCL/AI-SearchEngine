from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import os

# Ruta al archivo SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tablas (si no existen)
def init_db():
    Base.metadata.create_all(bind=engine)
