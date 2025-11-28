"""
Modelo SQLAlchemy para la entidad Doctor
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Doctor(Base):
    """
    Modelo de la tabla doctor.
    Almacena información de los doctores asociados a especialidades.
    """
    __tablename__ = "doctor"

    id_doctor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False, index=True)
    correo = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20))
    licencia = Column(String(50), unique=True, nullable=False, index=True)
    id_especialidad = Column(Integer, ForeignKey('especialidad.id_especialidad'), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    especialidad = relationship("Especialidad", back_populates="doctores")
    horarios = relationship("Horario", back_populates="doctor", cascade="all, delete-orphan")
    citas = relationship("CitaMedica", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor(id={self.id_doctor}, nombre='{self.nombre} {self.apellido}', licencia='{self.licencia}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_doctor": self.id_doctor,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "correo": self.correo,
            "telefono": self.telefono,
            "licencia": self.licencia,
            "id_especialidad": self.id_especialidad,
            "activo": self.activo,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }


class Especialidad(Base):
    """
    Modelo de la tabla especialidad.
    Catálogo de especialidades médicas disponibles.
    """
    __tablename__ = "especialidad"

    id_especialidad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    doctores = relationship("Doctor", back_populates="especialidad")

    def __repr__(self):
        return f"<Especialidad(id={self.id_especialidad}, nombre='{self.nombre}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_especialidad": self.id_especialidad,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }