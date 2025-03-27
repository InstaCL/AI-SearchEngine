
from database.database import Base, engine

print("🛠️ Creando todas las tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas.")