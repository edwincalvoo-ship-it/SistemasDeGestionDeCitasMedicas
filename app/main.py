"""
Aplicación principal FastAPI - Sistema de Gestión de Citas Médicas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.database import check_connection
from app.routers import (
    pacientes_api,
    doctores_api,
    auth_api,
    horarios_api,
    citas_api,
    historias_api,
    facturas_api,
    metodos_pago_api
)

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="Sistema de Gestión de Citas Médicas",
    description="API REST para gestión integral de citas médicas, pacientes, doctores y facturación",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_api.router)
app.include_router(pacientes_api.router)
app.include_router(doctores_api.router)
app.include_router(horarios_api.router)
app.include_router(citas_api.router)
app.include_router(historias_api.router)
app.include_router(facturas_api.router)
app.include_router(metodos_pago_api.router)

@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar la aplicación"""
    print("🚀 Iniciando Sistema de Gestión de Citas Médicas...")
    
    # Verificar conexión a base de datos
    if check_connection():
        print("✅ Conexión a base de datos MySQL exitosa")
    else:
        print("❌ Error: No se pudo conectar a la base de datos MySQL")
        print("   Verifica las credenciales en el archivo .env")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento ejecutado al cerrar la aplicación"""
    print("🛑 Cerrando Sistema de Gestión de Citas Médicas...")

@app.get("/", tags=["Health Check"])
def root():
    """
    Endpoint raíz para verificar que la API está funcionando.
    """
    return {
        "mensaje": "API Sistema de Gestión de Citas Médicas",
        "version": "1.0.0",
        "status": "online",
        "documentacion": "/docs"
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Endpoint para verificar el estado de salud de la API y conexión a base de datos.
    """
    db_status = "connected" if check_connection() else "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "version": "1.0.0"
    }

# Manejador global de excepciones
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global para capturar excepciones no controladas.
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Configuración del servidor
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    # Iniciar servidor
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )

