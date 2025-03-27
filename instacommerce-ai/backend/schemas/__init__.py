# __init__.py para schemas/
# Este archivo indica que este directorio es un paquete de Python

# Puedes dejarlo vacío o agregar importaciones explícitas si quieres facilitar los imports
from .schemas import (
    EmpresaRequest,
    EmpresaResponse,
    EmpresaRegisterRequest,
    LoginRequest,
    LoginResponse,
    CredencialesUpdate,
    EndpointProductosUpdate,
    AtributosSeleccionUpdate,
)

