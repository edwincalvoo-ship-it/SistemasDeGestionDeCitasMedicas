"""
Modelo SQLAlchemy para la entidad Paciente
"""
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func
from app.database import Base

class Paciente(Base):
    """
    Modelo de la tabla paciente.
    Almacena información personal de los pacientes del sistema.
    """
    __tablename__ = "paciente"

    id_paciente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False, index=True)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(255))
    fecha_nacimiento = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<Paciente(id={self.id_paciente}, nombre='{self.nombre} {self.apellido}', documento='{self.documento}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_paciente": self.id_paciente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_nacimiento": str(self.fecha_nacimiento) if self.fecha_nacimiento else None,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }