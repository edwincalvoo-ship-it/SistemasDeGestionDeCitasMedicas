from sqlalchemy.orm import Session
from app.repositories import facturas_repository, citas_repository
from app.schemas.factura import FacturaCreate
from fastapi import HTTPException

class FacturaService:
    @staticmethod
    def generar_factura(db: Session, factura_data: FacturaCreate):
        cita = citas_repository.get_by_id(db, factura_data.id_cita)
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        if cita.estado != 'completada':
            raise HTTPException(status_code=400, detail="Solo se pueden facturar citas completadas")
        if facturas_repository.get_by_cita(db, factura_data.id_cita):
            raise HTTPException(status_code=409, detail="Ya existe una factura para esta cita")
        return facturas_repository.create(db, factura_data)
    
    @staticmethod
    def obtener_factura(db: Session, factura_id: int):
        factura = facturas_repository.get_by_id(db, factura_id)
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")
        return factura
    
    @staticmethod
    def listar_facturas(db: Session, skip: int = 0, limit: int = 100):
        return facturas_repository.get_all(db, skip, limit)
    
    @staticmethod
    def listar_metodos_pago(db: Session):
        return facturas_repository.get_all_metodos_pago(db)
    
    @staticmethod
    def actualizar_estado_factura(db: Session, factura_id: int, estado: str):
        """Actualiza el estado de una factura"""
        factura = facturas_repository.get_by_id(db, factura_id)
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")
        return facturas_repository.update_estado(db, factura_id, estado)