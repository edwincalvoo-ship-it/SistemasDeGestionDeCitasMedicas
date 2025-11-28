"""
Servicio de lógica de negocio para Pacientes
"""
from sqlalchemy.orm import Session
from app.repositories import pacientes_repository
from app.schemas.paciente import PacienteCreate, PacienteUpdate
from app.models.paciente import Paciente
from app.models.usuario import Usuario
from typing import Optional, List
from fastapi import HTTPException
from passlib.context import CryptContext

# Configuración para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PacienteService:
    """Servicio para gestión de pacientes"""
    
    @staticmethod
    def crear_paciente(db: Session, paciente_data: PacienteCreate) -> Paciente:
        """
        Crea un nuevo paciente validando unicidad de documento y correo.
        También crea el usuario correspondiente en la tabla usuario.
        
        Args:
            db: Sesión de base de datos
            paciente_data: Datos del paciente a crear
            
        Returns:
            Paciente creado
            
        Raises:
            HTTPException: Si el documento o correo ya existen
        """
        # Validar que no exista el documento
        paciente_existente = pacientes_repository.get_by_documento(db, paciente_data.documento)
        if paciente_existente:
            raise HTTPException(
                status_code=409,
                detail="El documento ya se encuentra registrado"
            )
        
        # Validar que no exista el correo
        paciente_correo = pacientes_repository.get_by_correo(db, paciente_data.correo)
        if paciente_correo:
            raise HTTPException(
                status_code=409,
                detail="El correo electrónico ya se encuentra registrado"
            )
        
        # Validar que no exista el correo en la tabla usuario
        usuario_existente = db.query(Usuario).filter(Usuario.correo == paciente_data.correo).first()
        if usuario_existente:
            raise HTTPException(
                status_code=409,
                detail="El correo electrónico ya está registrado en el sistema"
            )
        
        # Crear paciente
        paciente = pacientes_repository.create(db, paciente_data)
        
        # Crear usuario asociado con contraseña = documento
        try:
            nuevo_usuario = Usuario(
                correo=paciente_data.correo,
                contrasena_hash=pwd_context.hash(paciente_data.documento),  # Campo correcto: contrasena_hash
                rol='paciente',
                activo=True,
                id_referencia=paciente.id_paciente  # Campo correcto: id_referencia
            )
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)
        except Exception as e:
            db.rollback()
            # Si falla la creación del usuario, eliminar el paciente creado
            db.delete(paciente)
            db.commit()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear el usuario: {str(e)}"
            )
        
        return paciente
    
    @staticmethod
    def obtener_paciente_por_id(db: Session, paciente_id: int) -> Optional[Paciente]:
        """
        Obtiene un paciente por su ID.
        
        Args:
            db: Sesión de base de datos
            paciente_id: ID del paciente
            
        Returns:
            Paciente encontrado o None
            
        Raises:
            HTTPException: Si el paciente no existe
        """
        paciente = pacientes_repository.get_by_id(db, paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )
        return paciente
    
    @staticmethod
    def obtener_todos_pacientes(db: Session, skip: int = 0, limit: int = 100) -> List[Paciente]:
        """
        Obtiene lista de pacientes con paginación.
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            Lista de pacientes
        """
        return pacientes_repository.get_all(db, skip, limit)
    
    @staticmethod
    def actualizar_paciente(db: Session, paciente_id: int, paciente_data: PacienteUpdate) -> Paciente:
        """
        Actualiza información de un paciente.
        
        Args:
            db: Sesión de base de datos
            paciente_id: ID del paciente a actualizar
            paciente_data: Datos a actualizar
            
        Returns:
            Paciente actualizado
            
        Raises:
            HTTPException: Si el paciente no existe o correo duplicado
        """
        paciente = pacientes_repository.get_by_id(db, paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )
        
        # Si se está actualizando el correo, validar que no exista
        if paciente_data.correo and paciente_data.correo != paciente.correo:
            paciente_correo = pacientes_repository.get_by_correo(db, paciente_data.correo)
            if paciente_correo:
                raise HTTPException(
                    status_code=409,
                    detail="El correo electrónico ya se encuentra registrado"
                )
        
        paciente_actualizado = pacientes_repository.update(db, paciente_id, paciente_data)
        return paciente_actualizado
    
    @staticmethod
    def eliminar_paciente(db: Session, paciente_id: int) -> bool:
        """
        Elimina un paciente del sistema.
        
        Args:
            db: Sesión de base de datos
            paciente_id: ID del paciente a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            HTTPException: Si el paciente no existe
        """
        paciente = pacientes_repository.get_by_id(db, paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )
        
        return pacientes_repository.delete(db, paciente_id)