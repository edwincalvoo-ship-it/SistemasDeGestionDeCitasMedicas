"""
Schemas Pydantic para autenticación y usuarios
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    """Schema para solicitud de login"""
    correo: EmailStr
    contrasena: str

    class Config:
        json_schema_extra = {
            "example": {
                "correo": "usuario@ejemplo.com",
                "contrasena": "password123"
            }
        }

class TokenResponse(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"
    usuario: dict

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "usuario": {
                    "id_usuario": 1,
                    "correo": "usuario@ejemplo.com",
                    "rol": "admin"
                }
            }
        }

class TokenData(BaseModel):
    """Schema para datos decodificados del token"""
    id_usuario: int
    correo: str
    rol: str

class UsuarioBase(BaseModel):
    """Schema base para usuario"""
    correo: EmailStr
    rol: str

class UsuarioCreate(UsuarioBase):
    """Schema para creación de usuario"""
    contrasena: str
    id_referencia: Optional[int] = None

class UsuarioResponse(UsuarioBase):
    """Schema para respuesta de usuario"""
    id_usuario: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True