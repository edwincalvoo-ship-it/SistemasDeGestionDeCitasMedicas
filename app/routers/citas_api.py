from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cita import CitaCreate, CitaUpdateEstado
from app.services.citas_service import CitaService
from app.dependencies.auth import require_any_authenticated

router = APIRouter(prefix="/api/citas", tags=["Citas"])

@router.post("", response_model=dict, status_code=status.HTTP_200_OK)
def registrar_cita(cita_data: CitaCreate, db: Session = Depends(get_db)):
    try:
        cita = CitaService.crear_cita(db, cita_data)
        return {"success": True, "mensaje": "Cita registrada con éxito", "data": {"id_cita": cita.id_cita}}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.get("", response_model=dict)
def listar_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        citas = CitaService.listar_citas(db, skip, limit)
        data = [{"id_cita": c.id_cita, "fecha": str(c.fecha), "hora": str(c.hora), 
                 "paciente": f"{c.paciente.nombre} {c.paciente.apellido}",
                 "doctor": f"{c.doctor.nombre} {c.doctor.apellido}", 
                 "estado": c.estado} for c in citas]
        return {"success": True, "mensaje": "Citas obtenidas", "data": data}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.get("/{cita_id}", response_model=dict)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    try:
        cita = CitaService.obtener_cita(db, cita_id)
        return {"success": True, "mensaje": "Cita encontrada", "data": cita.to_dict()}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.put("/actualizar_estado", response_model=dict)
def actualizar_estado_cita(data: CitaUpdateEstado, db: Session = Depends(get_db)):
    try:
        cita = CitaService.actualizar_estado(db, data.id_cita, data.estado)
        return {"success": True, "mensaje": "Estado actualizado", "data": {"estado": cita.estado}}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.put("/{id_cita}/estado", response_model=dict)
def actualizar_estado_cita_nuevo(id_cita: int, estado_data: dict, db: Session = Depends(get_db)):
    """
    Actualiza el estado de una cita médica.
    
    Args:
        id_cita: ID de la cita
        estado_data: Diccionario con el nuevo estado {"estado": "confirmada|completada|cancelada"}
    """
    try:
        estado = estado_data.get("estado")
        if not estado:
            return {"success": False, "mensaje": "Estado no proporcionado", "error_code": 400}
        
        if estado not in ['pendiente', 'confirmada', 'completada', 'cancelada']:
            return {"success": False, "mensaje": "Estado inválido", "error_code": 400}
        
        cita = CitaService.actualizar_estado(db, id_cita, estado)
        return {"success": True, "mensaje": "Estado actualizado exitosamente", "data": {"estado": cita.estado}}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except Exception as e:
        return {"success": False, "mensaje": f"Error interno: {str(e)}", "error_code": 500}
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.delete("/{cita_id}", response_model=dict)
def cancelar_cita(cita_id: int, db: Session = Depends(get_db)):
    try:
        CitaService.cancelar_cita(db, cita_id)
        return {"success": True, "mensaje": "Cita cancelada", "data": None}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}