from sqlalchemy.orm import Session, joinedload
from app.models.factura import Factura, MetodoPago
from app.schemas.factura import FacturaCreate
from typing import List, Optional

def create(db: Session, factura_data: FacturaCreate) -> Factura:
    factura = Factura(**factura_data.dict())
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura

def get_by_id(db: Session, factura_id: int) -> Optional[Factura]:
    return db.query(Factura).options(
        joinedload(Factura.cita),
        joinedload(Factura.metodo_pago)
    ).filter(Factura.id_factura == factura_id).first()

def get_by_cita(db: Session, cita_id: int) -> Optional[Factura]:
    return db.query(Factura).filter(Factura.id_cita == cita_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Factura]:
    return db.query(Factura).offset(skip).limit(limit).all()

def get_all_metodos_pago(db: Session) -> List[MetodoPago]:
    return db.query(MetodoPago).filter(MetodoPago.activo == True).all()

def update_estado(db: Session, factura_id: int, estado: str) -> Factura:
    """Actualiza el estado de una factura"""
    factura = db.query(Factura).filter(Factura.id_factura == factura_id).first()
    if factura:
        factura.estado = estado
        db.commit()
        db.refresh(factura)
    return factura