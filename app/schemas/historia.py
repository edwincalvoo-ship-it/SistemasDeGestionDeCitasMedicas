from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HistoriaCreate(BaseModel):
    id_paciente: int = Field(..., gt=0)
    id_doctor: int = Field(..., gt=0)
    id_cita: Optional[int] = None
    diagnostico: str = Field(..., min_length=5)
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id_paciente": 1,
                "id_doctor": 1,
                "id_cita": 1,
                "diagnostico": "Paciente en buen estado de salud",
                "tratamiento": "Continuar con hábitos saludables",
                "observaciones": "Control anual"
            }
        }

class HistoriaResponse(BaseModel):
    id_historia: int
    id_paciente: int
    id_doctor: int
    id_cita: Optional[int]
    fecha_registro: datetime
    diagnostico: str
    tratamiento: Optional[str]
    observaciones: Optional[str]

    class Config:
        from_attributes = True