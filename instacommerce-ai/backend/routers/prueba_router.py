from fastapi import APIRouter

router = APIRouter()

@router.get("/ping-test")
def ping_test():
    print("✅ Router de prueba activo")
    return {"mensaje": "pong-test"}
