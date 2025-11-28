"""
Modelo SQLAlchemy para la entidad Cita Médica
"""
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, TIMESTAMP, func, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EstadoCita(str, enum.Enum):
    """Enumeración de estados de cita"""
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class CitaMedica(Base):
    """
    Modelo de la tabla cita_medica.
    Almacena las citas médicas agendadas entre pacientes y doctores.
    """
    __tablename__ = "cita_medica"

    id_cita = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey('paciente.id_paciente', ondelete='CASCADE'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('doctor.id_doctor', ondelete='CASCADE'), nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    hora = Column(Time, nullable=False)
    motivo = Column(String(255), nullable=False)
    estado = Column(
        SQLEnum('pendiente', 'confirmada', 'completada', 'cancelada', name='estado_cita_enum'),
        default='pendiente',
        index=True
    )
    observaciones = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    paciente = relationship("Paciente", foreign_keys=[id_paciente])
    doctor = relationship("Doctor", back_populates="citas", foreign_keys=[id_doctor])
    historias = relationship("HistoriaClinica", back_populates="cita")
    facturas = relationship("Factura", back_populates="cita")

    def __repr__(self):
        return f"<CitaMedica(id={self.id_cita}, paciente_id={self.id_paciente}, doctor_id={self.id_doctor}, fecha='{self.fecha}', estado='{self.estado}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_cita": self.id_cita,
            "id_paciente": self.id_paciente,
            "id_doctor": self.id_doctor,
            "fecha": str(self.fecha) if self.fecha else None,
            "hora": str(self.hora) if self.hora else None,
            "motivo": self.motivo,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }