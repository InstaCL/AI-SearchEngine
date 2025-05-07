import os
from dotenv import load_dotenv

# Obtener la ruta absoluta del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    # Configuración de la API de OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Configuración de Pinecone
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")
    PINECONE_DIMENSIONS = int(os.getenv("PINECONE_DIMENSIONS", 3072))

    # Configuración de la API de productos
    PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL")

    def validate(self):
        if not all([
            self.OPENAI_API_KEY,
            self.PINECONE_API_KEY,
            self.PINECONE_ENV,
            self.PINECONE_INDEX,
            self.PRODUCTS_API_URL,
        ]):
            print("⚠️ Advertencia: Algunas variables de entorno están vacías. Verifica tu archivo .env")
        else:
            print("✅ Variables de entorno cargadas correctamente")

# Instancia única
settings = Settings()
settings.validate()
