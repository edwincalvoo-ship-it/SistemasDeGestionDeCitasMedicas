"""
Repositorio para operaciones CRUD de Horarios
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.horario import Horario
from app.schemas.horario import HorarioCreate, HorarioUpdate
from typing import Optional, List
from datetime import time

def create(db: Session, horario_data: HorarioCreate) -> Horario:
    """Crea un nuevo horario"""
    horario = Horario(
        id_doctor=horario_data.id_doctor,
        dia_semana=horario_data.dia_semana,
        hora_inicio=horario_data.hora_inicio,
        hora_fin=horario_data.hora_fin,
        activo=True
    )
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

def get_by_id(db: Session, horario_id: int) -> Optional[Horario]:
    """Obtiene un horario por ID"""
    return db.query(Horario).filter(Horario.id_horario == horario_id).first()

def get_by_doctor(db: Session, doctor_id: int) -> List[Horario]:
    """Obtiene todos los horarios de un doctor"""
    return db.query(Horario).filter(
        Horario.id_doctor == doctor_id,
        Horario.activo == True
    ).all()

def verificar_solapamiento(
    db: Session,
    doctor_id: int,
    dia_semana: str,
    hora_inicio: time,
    hora_fin: time,
    horario_id_excluir: Optional[int] = None
) -> bool:
    """Verifica si hay solapamiento de horarios para un doctor en un día"""
    query = db.query(Horario).filter(
        Horario.id_doctor == doctor_id,
        Horario.dia_semana == dia_semana,
        Horario.activo == True,
        # Condición de solapamiento: los rangos se intersectan
        and_(
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio
        )
    )
    
    if horario_id_excluir:
        query = query.filter(Horario.id_horario != horario_id_excluir)
    
    return query.first() is not None

def update(db: Session, horario_id: int, horario_data: HorarioUpdate) -> Horario:
    """Actualiza un horario"""
    horario = get_by_id(db, horario_id)
    if horario:
        update_data = horario_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(horario, key, value)
        db.commit()
        db.refresh(horario)
    return horario

def delete(db: Session, horario_id: int) -> bool:
    """Elimina un horario"""
    horario = get_by_id(db, horario_id)
    if horario:
        db.delete(horario)
        db.commit()
        return True
    return False