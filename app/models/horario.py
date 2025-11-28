"""
Modelo SQLAlchemy para la entidad Horario
"""
from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey, TIMESTAMP, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class DiaSemana(str, enum.Enum):
    """Enumeración de días de la semana"""
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"
    DOMINGO = "Domingo"

class Horario(Base):
    """
    Modelo de la tabla horario.
    Define los horarios de atención de cada doctor.
    """
    __tablename__ = "horario"

    id_horario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_doctor = Column(Integer, ForeignKey('doctor.id_doctor', ondelete='CASCADE'), nullable=False)
    dia_semana = Column(
        SQLEnum('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo', name='dia_semana_enum'),
        nullable=False
    )
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    doctor = relationship("Doctor", back_populates="horarios")

    def __repr__(self):
        return f"<Horario(id={self.id_horario}, doctor_id={self.id_doctor}, dia='{self.dia_semana}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_horario": self.id_horario,
            "id_doctor": self.id_doctor,
            "dia_semana": self.dia_semana,
            "hora_inicio": str(self.hora_inicio) if self.hora_inicio else None,
            "hora_fin": str(self.hora_fin) if self.hora_fin else None,
            "activo": self.activo,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }