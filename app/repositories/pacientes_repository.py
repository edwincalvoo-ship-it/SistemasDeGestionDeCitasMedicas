"""
Repositorio para operaciones CRUD de Pacientes
"""
from sqlalchemy.orm import Session
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate
from typing import Optional, List

def create(db: Session, paciente_data: PacienteCreate) -> Paciente:
    """
    Crea un nuevo paciente en la base de datos.
    
    Args:
        db: Sesión de base de datos
        paciente_data: Datos del paciente a crear
        
    Returns:
        Paciente creado
    """
    paciente = Paciente(
        nombre=paciente_data.nombre,
        apellido=paciente_data.apellido,
        documento=paciente_data.documento,
        correo=paciente_data.correo,
        telefono=paciente_data.telefono,
        direccion=paciente_data.direccion,
        fecha_nacimiento=paciente_data.fecha_nacimiento
    )
    
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    
    return paciente

def get_by_id(db: Session, paciente_id: int) -> Optional[Paciente]:
    """
    Obtiene un paciente por su ID.
    
    Args:
        db: Sesión de base de datos
        paciente_id: ID del paciente
        
    Returns:
        Paciente encontrado o None
    """
    return db.query(Paciente).filter(Paciente.id_paciente == paciente_id).first()

def get_by_documento(db: Session, documento: str) -> Optional[Paciente]:
    """
    Obtiene un paciente por su número de documento.
    
    Args:
        db: Sesión de base de datos
        documento: Número de documento
        
    Returns:
        Paciente encontrado o None
    """
    return db.query(Paciente).filter(Paciente.documento == documento).first()

def get_by_correo(db: Session, correo: str) -> Optional[Paciente]:
    """
    Obtiene un paciente por su correo electrónico.
    
    Args:
        db: Sesión de base de datos
        correo: Correo electrónico
        
    Returns:
        Paciente encontrado o None
    """
    return db.query(Paciente).filter(Paciente.correo == correo).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Paciente]:
    """
    Obtiene lista de pacientes con paginación.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Límite de registros a retornar
        
    Returns:
        Lista de pacientes
    """
    return db.query(Paciente).offset(skip).limit(limit).all()

def update(db: Session, paciente_id: int, paciente_data: PacienteUpdate) -> Paciente:
    """
    Actualiza información de un paciente.
    
    Args:
        db: Sesión de base de datos
        paciente_id: ID del paciente
        paciente_data: Datos a actualizar
        
    Returns:
        Paciente actualizado
    """
    paciente = get_by_id(db, paciente_id)
    
    if paciente:
        # Actualizar solo campos proporcionados
        update_data = paciente_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(paciente, key, value)
        
        db.commit()
        db.refresh(paciente)
    
    return paciente

def delete(db: Session, paciente_id: int) -> bool:
    """
    Elimina un paciente de la base de datos.
    
    Args:
        db: Sesión de base de datos
        paciente_id: ID del paciente
        
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    paciente = get_by_id(db, paciente_id)
    
    if paciente:
        db.delete(paciente)
        db.commit()
        return True
    
    return False