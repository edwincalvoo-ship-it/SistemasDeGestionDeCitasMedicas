
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.facturas_service import FacturaService

router = APIRouter(prefix="/api/metodos-pago", tags=["Métodos de Pago"])

@router.get("", response_model=dict)
def listar_metodos_pago(db: Session = Depends(get_db)):
    try:
        metodos = FacturaService.listar_metodos_pago(db)
        data = [{"id_metodo_pago": m.id_metodo_pago, "nombre": m.nombre} for m in metodos]
        return {"success": True, "mensaje": "Métodos de pago disponibles", "data": data}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}