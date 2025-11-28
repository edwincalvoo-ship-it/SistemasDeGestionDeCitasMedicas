"""
Schemas Pydantic para Cita Médica
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, time, datetime

class CitaBase(BaseModel):
    """Schema base para cita médica"""
    id_paciente: int = Field(..., gt=0)
    id_doctor: int = Field(..., gt=0)
    fecha: date = Field(..., description="Fecha de la cita en formato YYYY-MM-DD")
    hora: time = Field(..., description="Hora de la cita en formato HH:MM")
    motivo: str = Field(..., min_length=5, max_length=255)

    @validator('fecha')
    def validar_fecha(cls, v):
        """Valida que la fecha no sea del pasado"""
        if v < date.today():
            raise ValueError('La fecha de la cita no puede ser del pasado')
        return v

    @validator('hora')
    def validar_hora(cls, v):
        """Valida formato de hora"""
        return v

class CitaCreate(CitaBase):
    """Schema para creación de cita"""
    observaciones: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id_paciente": 1,
                "id_doctor": 1,
                "fecha": "2025-12-01",
                "hora": "09:00:00",
                "motivo": "Control rutinario",
                "observaciones": "Primera cita del paciente"
            }
        }

class CitaUpdate(BaseModel):
    """Schema para actualización de cita"""
    fecha: Optional[date] = None
    hora: Optional[time] = None
    motivo: Optional[str] = Field(None, min_length=5, max_length=255)
    observaciones: Optional[str] = None

class CitaUpdateEstado(BaseModel):
    """Schema para actualización de estado de cita"""
    id_cita: int = Field(..., gt=0)
    estado: str = Field(..., pattern="^(pendiente|confirmada|completada|cancelada)$")

    class Config:
        json_schema_extra = {
            "example": {
                "id_cita": 1,
                "estado": "confirmada"
            }
        }

class CitaResponse(CitaBase):
    """Schema para respuesta de cita"""
    id_cita: int
    estado: str
    observaciones: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CitaDetailResponse(CitaResponse):
    """Schema para respuesta detallada de cita con información del paciente y doctor"""
    paciente_nombre: Optional[str] = None
    paciente_apellido: Optional[str] = None
    doctor_nombre: Optional[str] = None
    doctor_apellido: Optional[str] = None
    especialidad: Optional[str] = None