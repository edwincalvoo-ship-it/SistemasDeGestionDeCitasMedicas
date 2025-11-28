"""
Dependencias de autenticación y autorización
"""

from app.dependencies.auth import (
    get_current_user,
    require_role,
    require_admin,
    require_doctor,
    require_any_authenticated
)

__all__ = [
    "get_current_user",
    "require_role",
    "require_admin",
    "require_doctor",
    "require_any_authenticated"
]