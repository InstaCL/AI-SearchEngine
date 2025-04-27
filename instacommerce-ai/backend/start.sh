#!/bin/bash

# Activar virtualenv si lo necesitas
# source venv/bin/activate

# Ejecutar el servidor FastAPI con Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
