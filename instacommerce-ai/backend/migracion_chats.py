from backend.database.database import engine, Base
from backend.database.models import Chat, ChatMensaje

print("🛠️ Creando tablas Chat y ChatMensaje...")
Base.metadata.create_all(bind=engine)
print("✅ Migración completada.")