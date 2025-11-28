"""
Schemas Pydantic para Doctor
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

class DoctorBase(BaseModel):
    """Schema base para doctor"""
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    documento: str = Field(..., min_length=5, max_length=20)
    correo: EmailStr
    telefono: Optional[str] = Field(None, min_length=7, max_length=20)
    licencia: str = Field(..., min_length=5, max_length=50)
    id_especialidad: int = Field(..., gt=0)

    @validator('correo')
    def validar_correo(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Formato de correo electrónico inválido')
        return v.lower()

class DoctorCreate(DoctorBase):
    """Schema para creación de doctor"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Laura",
                "apellido": "Martínez",
                "documento": "98765432",
                "correo": "laura.martinez@clinica.com",
                "telefono": "3001234567",
                "licencia": "MED-2023-010",
                "id_especialidad": 2
            }
        }

class DoctorUpdate(BaseModel):
    """Schema para actualización de doctor"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, min_length=7, max_length=20)
    id_especialidad: Optional[int] = Field(None, gt=0)
    activo: Optional[bool] = None

class DoctorResponse(DoctorBase):
    """Schema para respuesta de doctor"""
    id_doctor: int
    activo: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DoctorWithEspecialidad(DoctorResponse):
    """Schema para doctor con información de especialidad"""
    especialidad_nombre: Optional[str] = None

class EspecialidadResponse(BaseModel):
    """Schema para respuesta de especialidad"""
    id_especialidad: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True