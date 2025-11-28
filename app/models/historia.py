"""
Modelo SQLAlchemy para la entidad Historia Clínica
"""
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.orm import relationship
from app.database import Base

class HistoriaClinica(Base):
    """
    Modelo de la tabla historia_clinica.
    Almacena el historial médico de los pacientes.
    """
    __tablename__ = "historia_clinica"

    id_historia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey('paciente.id_paciente', ondelete='CASCADE'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('doctor.id_doctor', ondelete='CASCADE'), nullable=False)
    id_cita = Column(Integer, ForeignKey('cita_medica.id_cita', ondelete='SET NULL'))
    fecha_registro = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text)
    observaciones = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    paciente = relationship("Paciente", foreign_keys=[id_paciente])
    doctor = relationship("Doctor", foreign_keys=[id_doctor])
    cita = relationship("CitaMedica", back_populates="historias", foreign_keys=[id_cita])

    def __repr__(self):
        return f"<HistoriaClinica(id={self.id_historia}, paciente_id={self.id_paciente}, doctor_id={self.id_doctor})>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_historia": self.id_historia,
            "id_paciente": self.id_paciente,
            "id_doctor": self.id_doctor,
            "id_cita": self.id_cita,
            "fecha_registro": str(self.fecha_registro) if self.fecha_registro else None,
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "observaciones": self.observaciones,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }