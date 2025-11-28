"""
Configuración de base de datos MySQL con SQLAlchemy
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales de base de datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin1234")
DB_NAME = os.getenv("DB_NAME", "gestion_citas_medicas")

# Construir URL de conexión MySQL (usa pymysql)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False
)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos declarativos
Base = declarative_base()

def get_db():
    """
    Generador de dependencia para obtener sesión de base de datos.
    Uso:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa todas las tablas en la base de datos.
    Nota: En producción, usar migraciones con Alembic.
    """
    # Importar todos los modelos aquí para que SQLAlchemy los registre
    from app.models import paciente, doctor, cita, horario, usuario, historia, factura
    
    Base.metadata.create_all(bind=engine)

def check_connection():
    """
    Verifica la conexión a la base de datos.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        with engine.connect() as connection:
            # Usar sqlalchemy.text para que sea un objeto ejecutable
            result = connection.execute(text("SELECT 1"))
            # En SQLAlchemy moderno, result.scalar() devuelve el valor single
            val = result.scalar()
            return val == 1 or val == '1'
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return False