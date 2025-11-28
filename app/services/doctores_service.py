"""
Servicio de lógica de negocio para Doctores
"""
from sqlalchemy.orm import Session
from app.repositories import doctores_repository
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.models.doctor import Doctor
from typing import Optional, List
from fastapi import HTTPException

class DoctorService:
    """Servicio para gestión de doctores"""
    
    @staticmethod
    def crear_doctor(db: Session, doctor_data: DoctorCreate) -> Doctor:
        """
        Crea un nuevo doctor validando unicidad de documento, licencia y correo.
        
        Args:
            db: Sesión de base de datos
            doctor_data: Datos del doctor a crear
            
        Returns:
            Doctor creado
            
        Raises:
            HTTPException: Si el documento, licencia o correo ya existen, 
                          o si la especialidad no existe
        """
        # Validar que no exista el documento
        doctor_existente = doctores_repository.get_by_documento(db, doctor_data.documento)
        if doctor_existente:
            raise HTTPException(
                status_code=409,
                detail="El documento ya se encuentra registrado"
            )
        
        # Validar que no exista la licencia
        doctor_licencia = doctores_repository.get_by_licencia(db, doctor_data.licencia)
        if doctor_licencia:
            raise HTTPException(
                status_code=409,
                detail="La licencia médica ya se encuentra registrada"
            )
        
        # Validar que no exista el correo
        doctor_correo = doctores_repository.get_by_correo(db, doctor_data.correo)
        if doctor_correo:
            raise HTTPException(
                status_code=409,
                detail="El correo electrónico ya se encuentra registrado"
            )
        
        # Validar que la especialidad exista
        especialidad = doctores_repository.get_especialidad_by_id(db, doctor_data.id_especialidad)
        if not especialidad:
            raise HTTPException(
                status_code=404,
                detail="La especialidad especificada no existe"
            )
        
        # Crear doctor
        doctor = doctores_repository.create(db, doctor_data)
        return doctor
    
    @staticmethod
    def obtener_doctor_por_id(db: Session, doctor_id: int) -> Optional[Doctor]:
        """
        Obtiene un doctor por su ID.
        
        Args:
            db: Sesión de base de datos
            doctor_id: ID del doctor
            
        Returns:
            Doctor encontrado o None
            
        Raises:
            HTTPException: Si el doctor no existe
        """
        doctor = doctores_repository.get_by_id(db, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor no encontrado"
            )
        return doctor
    
    @staticmethod
    def obtener_todos_doctores(db: Session, skip: int = 0, limit: int = 100) -> List[Doctor]:
        """
        Obtiene lista de doctores con paginación.
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            Lista de doctores
        """
        return doctores_repository.get_all(db, skip, limit)
    
    @staticmethod
    def obtener_doctores_por_especialidad(db: Session, especialidad_id: int) -> List[Doctor]:
        """
        Obtiene doctores por especialidad.
        
        Args:
            db: Sesión de base de datos
            especialidad_id: ID de la especialidad
            
        Returns:
            Lista de doctores de esa especialidad
        """
        return doctores_repository.get_by_especialidad(db, especialidad_id)
    
    @staticmethod
    def actualizar_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate) -> Doctor:
        """
        Actualiza información de un doctor.
        
        Args:
            db: Sesión de base de datos
            doctor_id: ID del doctor a actualizar
            doctor_data: Datos a actualizar
            
        Returns:
            Doctor actualizado
            
        Raises:
            HTTPException: Si el doctor no existe, correo duplicado o especialidad inválida
        """
        doctor = doctores_repository.get_by_id(db, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor no encontrado"
            )
        
        # Si se está actualizando el correo, validar que no exista
        if doctor_data.correo and doctor_data.correo != doctor.correo:
            doctor_correo = doctores_repository.get_by_correo(db, doctor_data.correo)
            if doctor_correo:
                raise HTTPException(
                    status_code=409,
                    detail="El correo electrónico ya se encuentra registrado"
                )
        
        # Si se está actualizando la especialidad, validar que exista
        if doctor_data.id_especialidad:
            especialidad = doctores_repository.get_especialidad_by_id(db, doctor_data.id_especialidad)
            if not especialidad:
                raise HTTPException(
                    status_code=404,
                    detail="La especialidad especificada no existe"
                )
        
        doctor_actualizado = doctores_repository.update(db, doctor_id, doctor_data)
        return doctor_actualizado
    
    @staticmethod
    def eliminar_doctor(db: Session, doctor_id: int) -> bool:
        """
        Elimina un doctor del sistema.
        
        Args:
            db: Sesión de base de datos
            doctor_id: ID del doctor a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            HTTPException: Si el doctor no existe
        """
        doctor = doctores_repository.get_by_id(db, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor no encontrado"
            )
        
        return doctores_repository.delete(db, doctor_id)
    
    @staticmethod
    def obtener_especialidades(db: Session):
        """
        Obtiene todas las especialidades disponibles.
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            Lista de especialidades
        """
        return doctores_repository.get_all_especialidades(db)