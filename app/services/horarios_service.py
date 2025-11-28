"""
Servicio de lógica de negocio para Horarios
"""
from sqlalchemy.orm import Session
from app.repositories import horarios_repository, doctores_repository
from app.schemas.horario import HorarioCreate, HorarioUpdate
from app.models.horario import Horario
from typing import List
from fastapi import HTTPException

class HorarioService:
    """Servicio para gestión de horarios"""
    
    @staticmethod
    def crear_horario(db: Session, horario_data: HorarioCreate) -> Horario:
        """Crea un nuevo horario validando doctor y solapamiento"""
        # Validar que el doctor exista
        doctor = doctores_repository.get_by_id(db, horario_data.id_doctor)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor no encontrado")
        
        # Verificar solapamiento
        hay_solapamiento = horarios_repository.verificar_solapamiento(
            db,
            horario_data.id_doctor,
            horario_data.dia_semana,
            horario_data.hora_inicio,
            horario_data.hora_fin
        )
        
        if hay_solapamiento:
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe un horario que se solapa con el horario propuesto para el día {horario_data.dia_semana}"
            )
        
        return horarios_repository.create(db, horario_data)
    
    @staticmethod
    def obtener_horarios_doctor(db: Session, doctor_id: int) -> List[Horario]:
        """Obtiene todos los horarios de un doctor"""
        doctor = doctores_repository.get_by_id(db, doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor no encontrado")
        
        return horarios_repository.get_by_doctor(db, doctor_id)
    
    @staticmethod
    def actualizar_horario(db: Session, horario_id: int, horario_data: HorarioUpdate) -> Horario:
        """Actualiza un horario"""
        horario = horarios_repository.get_by_id(db, horario_id)
        if not horario:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        
        # Si se actualizan horas, verificar solapamiento
        if horario_data.hora_inicio or horario_data.hora_fin or horario_data.dia_semana:
            hora_inicio = horario_data.hora_inicio or horario.hora_inicio
            hora_fin = horario_data.hora_fin or horario.hora_fin
            dia_semana = horario_data.dia_semana or horario.dia_semana
            
            hay_solapamiento = horarios_repository.verificar_solapamiento(
                db, horario.id_doctor, dia_semana, hora_inicio, hora_fin, horario_id
            )
            
            if hay_solapamiento:
                raise HTTPException(status_code=409, detail="Solapamiento de horarios detectado")
        
        return horarios_repository.update(db, horario_id, horario_data)
    
    @staticmethod
    def eliminar_horario(db: Session, horario_id: int) -> bool:
        """Elimina un horario"""
        horario = horarios_repository.get_by_id(db, horario_id)
        if not horario:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        
        return horarios_repository.delete(db, horario_id)