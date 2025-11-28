"""
Router API para gestión de Horarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.horario import HorarioCreate, HorarioUpdate, HorarioResponse
from app.services.horarios_service import HorarioService
from app.dependencies.auth import require_admin

router = APIRouter(prefix="/api/horarios", tags=["Horarios"])

@router.post("", response_model=dict, status_code=status.HTTP_200_OK)
def registrar_horario(
    horario_data: HorarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """[HU-003] Registrar horario (requiere admin)"""
    try:
        horario = HorarioService.crear_horario(db, horario_data)
        return {
            "success": True,
            "mensaje": "Horario registrado con éxito",
            "data": {
                "id_horario": horario.id_horario,
                "id_doctor": horario.id_doctor,
                "dia_semana": horario.dia_semana,
                "hora_inicio": str(horario.hora_inicio),
                "hora_fin": str(horario.hora_fin)
            }
        }
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except Exception:
        return {"success": False, "mensaje": "Error interno en el servidor", "error_code": 500}

@router.get("/doctor/{doctor_id}", response_model=dict)
def obtener_horarios_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Obtiene horarios de un doctor"""
    try:
        horarios = HorarioService.obtener_horarios_doctor(db, doctor_id)
        horarios_data = [{
            "id_horario": h.id_horario,
            "dia_semana": h.dia_semana,
            "hora_inicio": str(h.hora_inicio),
            "hora_fin": str(h.hora_fin),
            "activo": h.activo
        } for h in horarios]
        return {"success": True, "mensaje": "Horarios obtenidos", "data": horarios_data}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except Exception:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}