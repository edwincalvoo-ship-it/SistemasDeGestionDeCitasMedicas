"""
Repositorio para operaciones CRUD de Doctores
"""
from sqlalchemy.orm import Session, joinedload
from app.models.doctor import Doctor, Especialidad
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from typing import Optional, List

def create(db: Session, doctor_data: DoctorCreate) -> Doctor:
    """
    Crea un nuevo doctor en la base de datos.
    
    Args:
        db: Sesión de base de datos
        doctor_data: Datos del doctor a crear
        
    Returns:
        Doctor creado
    """
    doctor = Doctor(
        nombre=doctor_data.nombre,
        apellido=doctor_data.apellido,
        documento=doctor_data.documento,
        correo=doctor_data.correo,
        telefono=doctor_data.telefono,
        licencia=doctor_data.licencia,
        id_especialidad=doctor_data.id_especialidad,
        activo=True
    )
    
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    
    return doctor

def get_by_id(db: Session, doctor_id: int) -> Optional[Doctor]:
    """
    Obtiene un doctor por su ID con información de especialidad.
    
    Args:
        db: Sesión de base de datos
        doctor_id: ID del doctor
        
    Returns:
        Doctor encontrado o None
    """
    return db.query(Doctor)\
        .options(joinedload(Doctor.especialidad))\
        .filter(Doctor.id_doctor == doctor_id)\
        .first()

def get_by_documento(db: Session, documento: str) -> Optional[Doctor]:
    """
    Obtiene un doctor por su número de documento.
    
    Args:
        db: Sesión de base de datos
        documento: Número de documento
        
    Returns:
        Doctor encontrado o None
    """
    return db.query(Doctor).filter(Doctor.documento == documento).first()

def get_by_licencia(db: Session, licencia: str) -> Optional[Doctor]:
    """
    Obtiene un doctor por su número de licencia médica.
    
    Args:
        db: Sesión de base de datos
        licencia: Número de licencia
        
    Returns:
        Doctor encontrado o None
    """
    return db.query(Doctor).filter(Doctor.licencia == licencia).first()

def get_by_correo(db: Session, correo: str) -> Optional[Doctor]:
    """
    Obtiene un doctor por su correo electrónico.
    
    Args:
        db: Sesión de base de datos
        correo: Correo electrónico
        
    Returns:
        Doctor encontrado o None
    """
    return db.query(Doctor).filter(Doctor.correo == correo).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Doctor]:
    """
    Obtiene lista de doctores con paginación.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Límite de registros a retornar
        
    Returns:
        Lista de doctores
    """
    return db.query(Doctor)\
        .options(joinedload(Doctor.especialidad))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_by_especialidad(db: Session, especialidad_id: int) -> List[Doctor]:
    """
    Obtiene doctores por especialidad.
    
    Args:
        db: Sesión de base de datos
        especialidad_id: ID de la especialidad
        
    Returns:
        Lista de doctores de esa especialidad
    """
    return db.query(Doctor)\
        .filter(Doctor.id_especialidad == especialidad_id, Doctor.activo == True)\
        .all()

def update(db: Session, doctor_id: int, doctor_data: DoctorUpdate) -> Doctor:
    """
    Actualiza información de un doctor.
    
    Args:
        db: Sesión de base de datos
        doctor_id: ID del doctor
        doctor_data: Datos a actualizar
        
    Returns:
        Doctor actualizado
    """
    doctor = get_by_id(db, doctor_id)
    
    if doctor:
        # Actualizar solo campos proporcionados
        update_data = doctor_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(doctor, key, value)
        
        db.commit()
        db.refresh(doctor)
    
    return doctor

def delete(db: Session, doctor_id: int) -> bool:
    """
    Elimina un doctor de la base de datos.
    
    Args:
        db: Sesión de base de datos
        doctor_id: ID del doctor
        
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    doctor = get_by_id(db, doctor_id)
    
    if doctor:
        db.delete(doctor)
        db.commit()
        return True
    
    return False

# Funciones para especialidades
def get_all_especialidades(db: Session) -> List[Especialidad]:
    """
    Obtiene todas las especialidades disponibles.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        Lista de especialidades
    """
    return db.query(Especialidad).all()

def get_especialidad_by_id(db: Session, especialidad_id: int) -> Optional[Especialidad]:
    """
    Obtiene una especialidad por ID.
    
    Args:
        db: Sesión de base de datos
        especialidad_id: ID de la especialidad
        
    Returns:
        Especialidad encontrada o None
    """
    return db.query(Especialidad).filter(Especialidad.id_especialidad == especialidad_id).first()