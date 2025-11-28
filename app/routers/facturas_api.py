from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.factura import FacturaCreate
from app.services.facturas_service import FacturaService

router = APIRouter(prefix="/api/facturas", tags=["Facturación"])

@router.post("", response_model=dict, status_code=status.HTTP_200_OK)
def generar_factura(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    try:
        factura = FacturaService.generar_factura(db, factura_data)
        return {"success": True, "mensaje": "Factura generada", "data": {"id_factura": factura.id_factura}}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.get("", response_model=dict)
def listar_facturas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        facturas = FacturaService.listar_facturas(db, skip, limit)
        data = [{
            "id_factura": f.id_factura,
            "id_cita": f.id_cita,
            "id_metodo_pago": f.id_metodo_pago,
            "monto": float(f.monto),
            "estado": f.estado,
            "fecha_emision": str(f.fecha_emision) if f.fecha_emision else None,
            "observaciones": f.observaciones
        } for f in facturas]
        return {"success": True, "mensaje": "Facturas obtenidas", "data": data}
    except Exception as e:
        return {"success": False, "mensaje": f"Error interno: {str(e)}", "error_code": 500}

@router.get("/{factura_id}", response_model=dict)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    try:
        factura = FacturaService.obtener_factura(db, factura_id)
        return {"success": True, "mensaje": "Factura encontrada", "data": factura.to_dict()}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.put("/{factura_id}/estado", response_model=dict)
def actualizar_estado_factura(factura_id: int, estado_data: dict, db: Session = Depends(get_db)):
    """
    Actualiza el estado de una factura.
    Estados válidos: 'pagada', 'pendiente', 'anulada'
    """
    try:
        estado = estado_data.get("estado")
        if not estado:
            return {"success": False, "mensaje": "Estado no proporcionado", "error_code": 400}
        
        if estado not in ['pagada', 'pendiente', 'anulada']:
            return {"success": False, "mensaje": "Estado inválido", "error_code": 400}
        
        factura = FacturaService.actualizar_estado_factura(db, factura_id, estado)
        return {"success": True, "mensaje": "Estado actualizado exitosamente", "data": {"estado": factura.estado}}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except Exception as e:
        return {"success": False, "mensaje": f"Error interno: {str(e)}", "error_code": 500}