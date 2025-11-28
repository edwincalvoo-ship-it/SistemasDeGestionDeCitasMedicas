
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.historia import HistoriaCreate
from app.services.historias_service import HistoriaService
from app.dependencies.auth import require_doctor

router = APIRouter(prefix="/api/historias", tags=["Historias Clínicas"])

@router.post("", response_model=dict, status_code=status.HTTP_200_OK)
def crear_historia(
    historia_data: HistoriaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_doctor)
):
    try:
        historia = HistoriaService.crear_historia(db, historia_data)
        return {"success": True, "mensaje": "Historia clínica registrada", "data": {"id_historia": historia.id_historia}}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}

@router.get("/{paciente_id}", response_model=dict)
def obtener_historias(paciente_id: int, db: Session = Depends(get_db)):
    try:
        historias = HistoriaService.obtener_historias_paciente(db, paciente_id)
        data = [{
            "id_historia": h.id_historia,
            "fecha_registro": str(h.fecha_registro),
            "diagnostico": h.diagnostico,
            "tratamiento": h.tratamiento,
            "doctor": f"{h.doctor.nombre} {h.doctor.apellido}"
        } for h in historias]
        return {"success": True, "mensaje": "Historias obtenidas", "data": data}
    except HTTPException as e:
        return {"success": False, "mensaje": e.detail, "error_code": e.status_code}
    except:
        return {"success": False, "mensaje": "Error interno", "error_code": 500}