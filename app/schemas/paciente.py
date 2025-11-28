"""
Schemas Pydantic para Paciente
"""
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import date, datetime
import re

class PacienteBase(BaseModel):
    """Schema base para paciente"""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del paciente")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del paciente")
    documento: str = Field(..., min_length=5, max_length=20, description="Documento de identidad")
    correo: EmailStr = Field(..., description="Correo electrónico")
    telefono: str = Field(..., min_length=7, max_length=20, description="Número de teléfono")
    direccion: Optional[str] = Field(None, max_length=255, description="Dirección de residencia")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")

    @validator('correo')
    def validar_correo(cls, v):
        """Valida formato de correo electrónico"""
        # EmailStr de Pydantic ya valida, pero agregamos validación adicional si es necesario
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Formato de correo electrónico inválido')
        return v.lower()

    @validator('fecha_nacimiento')
    def validar_fecha_nacimiento(cls, v):
        """Valida que la fecha de nacimiento sea válida"""
        if v > date.today():
            raise ValueError('La fecha de nacimiento no puede ser futura')
        
        # Calcular edad
        edad = (date.today() - v).days // 365
        if edad > 120:
            raise ValueError('La fecha de nacimiento no es válida')
        
        return v

class PacienteCreate(PacienteBase):
    """Schema para creación de paciente"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "documento": "123456789",
                "correo": "juan.perez@email.com",
                "telefono": "3101234567",
                "direccion": "Calle 123 #45-67",
                "fecha_nacimiento": "1990-05-15"
            }
        }

class PacienteUpdate(BaseModel):
    """Schema para actualización de paciente"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, min_length=7, max_length=20)
    direccion: Optional[str] = Field(None, max_length=255)
    fecha_nacimiento: Optional[date] = None

    @validator('correo')
    def validar_correo(cls, v):
        """Valida formato de correo electrónico"""
        if v and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Formato de correo electrónico inválido')
        return v.lower() if v else v

class PacienteResponse(PacienteBase):
    """Schema para respuesta de paciente"""
    id_paciente: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_paciente": 1,
                "nombre": "Juan",
                "apellido": "Pérez",
                "documento": "123456789",
                "correo": "juan.perez@email.com",
                "telefono": "3101234567",
                "direccion": "Calle 123 #45-67",
                "fecha_nacimiento": "1990-05-15",
                "created_at": "2025-11-25T10:00:00",
                "updated_at": "2025-11-25T10:00:00"
            }
        }

class PacienteListResponse(BaseModel):
    """Schema para lista de pacientes"""
    id_paciente: int
    nombre: str
    apellido: str
    documento: str
    correo: str

    class Config:
        from_attributes = True