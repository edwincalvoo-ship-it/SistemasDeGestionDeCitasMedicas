
from sqlalchemy.orm import Session, joinedload
from app.models.historia import HistoriaClinica
from app.schemas.historia import HistoriaCreate
from typing import List

def create(db: Session, historia_data: HistoriaCreate) -> HistoriaClinica:
    historia = HistoriaClinica(**historia_data.dict())
    db.add(historia)
    db.commit()
    db.refresh(historia)
    return historia

def get_by_paciente(db: Session, paciente_id: int) -> List[HistoriaClinica]:
    return db.query(HistoriaClinica).options(
        joinedload(HistoriaClinica.doctor)
    ).filter(HistoriaClinica.id_paciente == paciente_id).order_by(
        HistoriaClinica.fecha_registro.desc()
    ).all()

def get_by_id(db: Session, historia_id: int):
    return db.query(HistoriaClinica).filter(HistoriaClinica.id_historia == historia_id).first()