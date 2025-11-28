"""
Schemas Pydantic para Horario
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import time, datetime

class HorarioBase(BaseModel):
    """Schema base para horario"""
    id_doctor: int = Field(..., gt=0)
    dia_semana: str = Field(..., pattern="^(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)$")
    hora_inicio: time
    hora_fin: time

    @validator('hora_fin')
    def validar_hora_fin(cls, v, values):
        """Valida que hora_fin sea mayor que hora_inicio"""
        if 'hora_inicio' in values and v <= values['hora_inicio']:
            raise ValueError('La hora de fin debe ser mayor que la hora de inicio')
        return v

class HorarioCreate(HorarioBase):
    """Schema para creación de horario"""
    class Config:
        json_schema_extra = {
            "example": {
                "id_doctor": 1,
                "dia_semana": "Lunes",
                "hora_inicio": "08:00:00",
                "hora_fin": "12:00:00"
            }
        }

class HorarioUpdate(BaseModel):
    """Schema para actualización de horario"""
    dia_semana: Optional[str] = Field(None, pattern="^(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)$")
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    activo: Optional[bool] = None

class HorarioResponse(HorarioBase):
    """Schema para respuesta de horario"""
    id_horario: int
    activo: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True