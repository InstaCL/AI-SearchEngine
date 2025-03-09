from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DATABASE_URL = "sqlite:///./database.db"  # 📌 Base de datos SQLite

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔥 FORZAR LA CREACIÓN DE LA BASE DE DATOS
print("✅ Creando base de datos y tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente!")
