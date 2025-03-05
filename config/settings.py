import os
from dotenv import load_dotenv

# Obtener la ruta absoluta del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

# Cargar el archivo .env desde la ruta especificada
load_dotenv(dotenv_path=dotenv_path)

# Configuración de la API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuración de Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Configuración de la API de productos
PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL")

# Validar que las variables se cargaron correctamente
if not all([OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX, PRODUCTS_API_URL]):
    print("⚠️ Advertencia: Algunas variables de entorno están vacías. Verifica tu archivo .env")
else:
    print("✅ Variables de entorno cargadas correctamente")
