# test_db_connection.py

from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, engine
from backend.database.models import Empresa, Base

def test_connection():
    try:
        # Crear las tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("✅ Conexión a la base de datos establecida correctamente y tablas creadas.")

        # Abrir sesión
        db: Session = SessionLocal()

        # Prueba simple: consultar si hay empresas registradas
        empresas = db.query(Empresa).all()
        print(f"ℹ️ Empresas registradas actualmente: {len(empresas)}")

        db.close()

    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")

if __name__ == "__main__":
    test_connection()
