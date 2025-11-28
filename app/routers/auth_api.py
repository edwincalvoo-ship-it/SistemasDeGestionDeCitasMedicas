"""
Router API para Autenticación y Login JWT
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.user import LoginRequest, TokenResponse
from app.services.auth_service import verify_password, generate_user_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"]
)

@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    [HU-007] Endpoint para iniciar sesión y obtener token JWT.
    
    - **correo**: Correo electrónico del usuario (requerido)
    - **contrasena**: Contraseña del usuario (requerido)
    
    Retorna un token JWT válido por 24 horas y la información del usuario.
    """
    try:
        # Buscar usuario por correo
        usuario = db.query(Usuario).filter(Usuario.correo == credentials.correo).first()
        
        # Validar credenciales
        if not usuario:
            return {
                "success": False,
                "mensaje": "Credenciales inválidas",
                "error_code": 401
            }
        
        if not verify_password(credentials.contrasena, usuario.contrasena_hash):
            return {
                "success": False,
                "mensaje": "Credenciales inválidas",
                "error_code": 401
            }
        
        # Validar que el usuario esté activo
        if not usuario.activo:
            return {
                "success": False,
                "mensaje": "Usuario inactivo. Contacte al administrador.",
                "error_code": 401
            }
        
        # Generar token JWT
        token = generate_user_token(
            id_usuario=usuario.id_usuario,
            correo=usuario.correo,
            rol=usuario.rol
        )
        
        return {
            "success": True,
            "mensaje": "Login exitoso",
            "data": {
                "access_token": token,
                "token_type": "bearer",
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "correo": usuario.correo,
                    "rol": usuario.rol
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }