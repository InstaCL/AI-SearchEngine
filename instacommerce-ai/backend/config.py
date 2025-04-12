import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-super-secreta")
    ALGORITHM = "HS256"

settings = Settings()