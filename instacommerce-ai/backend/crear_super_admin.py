from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.database.models import Empresa
from passlib.context import CryptContext

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Datos del Super Admin
super_admin_data = {
    "nombre_empresa": "Super Admin",
    "rut": "99999999-9",
    "correo": "christopher.lara@instacommerce.cl",
    "tipo_productos": "Todos",
    "password_hash": pwd_context.hash("Insta2025_"),
    "estado_pago": "activo"
}

# Crear empresa si no existe
def crear_super_admin():
    db: Session = SessionLocal()

    existe = db.query(Empresa).filter(Empresa.correo == super_admin_data["correo"]).first()
    if existe:
        print("⚠️ El Super Admin ya existe en la base de datos.")
        return

    nuevo_admin = Empresa(**super_admin_data)
    db.add(nuevo_admin)
    db.commit()
    db.refresh(nuevo_admin)

    print("✅ Super Admin creado exitosamente:")
    print(f"   ➤ ID: {nuevo_admin.id}")
    print(f"   ➤ Correo: {nuevo_admin.correo}")
    print(f"   ➤ Alias: {nuevo_admin.nombre_empresa}")

if __name__ == "__main__":
    crear_super_admin()
