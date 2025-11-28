"""
Modelo SQLAlchemy para la entidad Usuario
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func, Enum as SQLEnum
from app.database import Base
import enum

class RolUsuario(str, enum.Enum):
    """Enumeración de roles de usuario"""
    ADMIN = "admin"
    DOCTOR = "doctor"
    PACIENTE = "paciente"

class Usuario(Base):
    """
    Modelo de la tabla usuario.
    Gestiona autenticación y autorización del sistema.
    """
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(
        SQLEnum('admin', 'doctor', 'paciente', name='rol_usuario_enum'),
        nullable=False,
        index=True
    )
    id_referencia = Column(Integer)  # Referencia a paciente o doctor según el rol
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, correo='{self.correo}', rol='{self.rol}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON (sin contraseña)"""
        return {
            "id_usuario": self.id_usuario,
            "correo": self.correo,
            "rol": self.rol,
            "id_referencia": self.id_referencia,
            "activo": self.activo,
            "created_at": str(self.created_at) if self.created_at else None
        }