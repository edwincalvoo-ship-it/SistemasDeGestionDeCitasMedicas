"""
Dependencias de autenticación y autorización
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import decode_access_token
from typing import List

# Configurar esquema de seguridad Bearer
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependencia para obtener el usuario actual desde el token JWT.
    
    Args:
        credentials: Credenciales del header Authorization
        
    Returns:
        dict: Datos del usuario decodificados del token
        
    Raises:
        HTTPException: Si el token es inválido o está expirado
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return payload

def require_role(allowed_roles: List[str]):
    """
    Factory de dependencia para verificar que el usuario tenga un rol específico.
    
    Args:
        allowed_roles: Lista de roles permitidos (ej: ["admin", "doctor"])
        
    Returns:
        Función de dependencia que valida el rol
        
    Example:
        @router.post("/doctores")
        def crear_doctor(
            current_user: dict = Depends(require_role(["admin"]))
        ):
            # Solo usuarios admin pueden acceder
            pass
    """
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("rol")
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permisos para realizar esta acción. Se requiere uno de estos roles: {', '.join(allowed_roles)}"
            )
        
        return current_user
    
    return role_checker

# Dependencias pre-configuradas para roles comunes
require_admin = require_role(["admin"])
require_doctor = require_role(["doctor", "admin"])
require_any_authenticated = get_current_user