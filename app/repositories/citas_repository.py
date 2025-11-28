from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from app.models.cita import CitaMedica
from app.schemas.cita import CitaCreate, CitaUpdate
from typing import Optional, List
from datetime import date, time

def create(db: Session, cita_data: CitaCreate) -> CitaMedica:
    cita = CitaMedica(**cita_data.dict())
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

def get_by_id(db: Session, cita_id: int) -> Optional[CitaMedica]:
    return db.query(CitaMedica).options(
        joinedload(CitaMedica.paciente),
        joinedload(CitaMedica.doctor)
    ).filter(CitaMedica.id_cita == cita_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[CitaMedica]:
    return db.query(CitaMedica).options(
        joinedload(CitaMedica.paciente),
        joinedload(CitaMedica.doctor)
    ).offset(skip).limit(limit).all()

def verificar_disponibilidad(db: Session, doctor_id: int, fecha: date, hora: time, cita_id_excluir: Optional[int] = None) -> bool:
    query = db.query(CitaMedica).filter(
        CitaMedica.id_doctor == doctor_id,
        CitaMedica.fecha == fecha,
        CitaMedica.hora == hora,
        CitaMedica.estado != 'cancelada'
    )
    if cita_id_excluir:
        query = query.filter(CitaMedica.id_cita != cita_id_excluir)
    return query.first() is None

def update_estado(db: Session, cita_id: int, estado: str) -> CitaMedica:
    cita = db.query(CitaMedica).filter(CitaMedica.id_cita == cita_id).first()
    if cita:
        cita.estado = estado
        db.commit()
        db.refresh(cita)
    return cita

def delete(db: Session, cita_id: int) -> bool:
    cita = get_by_id(db, cita_id)
    if cita:
        cita.estado = 'cancelada'
        db.commit()
        return True
    return False