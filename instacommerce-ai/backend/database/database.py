from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import os

# 🔁 Cambiar a db.sqlite3
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
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
