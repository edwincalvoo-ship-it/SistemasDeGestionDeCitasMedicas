from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Cargar variables del archivo .env
load_dotenv()

# Ejemplo: obtener variables de entorno
APP_NAME = os.getenv("APP_NAME")
DEBUG = os.getenv("DEBUG")
SECRET_KEY = os.getenv("SECRET_KEY")

# Crear la instancia de FastAPI
app = FastAPI(
    title=APP_NAME or "Mi API con FastAPI",
    description="API RESTful profesional",
    version="1.0.0"
)

# Ruta raíz
@app.get("/")
async def root():
    """
    Endpoint de bienvenida.
    """
    return {
        "message": f"¡Bienvenido a {APP_NAME or 'mi API con FastAPI'}!",
        "status": "online",
        "debug": DEBUG,
        "version": "1.0.0"
    }

# Endpoint con parámetros
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """
    Ejemplo con parámetros de ruta y query.
    """
    return {
        "item_id": item_id,
        "query": q
    }

# Health check
@app.get("/health")
async def health_check():
    """
    Verifica el estado del servidor.
    """
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"}
    )

#prueba github
