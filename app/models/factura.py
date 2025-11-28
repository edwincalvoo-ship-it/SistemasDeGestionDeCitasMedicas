"""
Modelo SQLAlchemy para la entidad Factura y Método de Pago
"""
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey, TIMESTAMP, func, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EstadoFactura(str, enum.Enum):
    """Enumeración de estados de factura"""
    PAGADA = "pagada"
    PENDIENTE = "pendiente"
    ANULADA = "anulada"

class Factura(Base):
    """
    Modelo de la tabla factura.
    Almacena la información de facturación de las citas médicas.
    """
    __tablename__ = "factura"

    id_factura = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cita = Column(Integer, ForeignKey('cita_medica.id_cita', ondelete='CASCADE'), nullable=False, unique=True)
    id_metodo_pago = Column(Integer, ForeignKey('metodo_pago.id_metodo_pago'), nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    fecha_emision = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    estado = Column(
        SQLEnum('pagada', 'pendiente', 'anulada', name='estado_factura_enum'),
        default='pendiente',
        index=True
    )
    observaciones = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    cita = relationship("CitaMedica", back_populates="facturas", foreign_keys=[id_cita])
    metodo_pago = relationship("MetodoPago", foreign_keys=[id_metodo_pago])

    def __repr__(self):
        return f"<Factura(id={self.id_factura}, cita_id={self.id_cita}, monto={self.monto}, estado='{self.estado}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_factura": self.id_factura,
            "id_cita": self.id_cita,
            "id_metodo_pago": self.id_metodo_pago,
            "monto": float(self.monto),
            "fecha_emision": str(self.fecha_emision) if self.fecha_emision else None,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }


class MetodoPago(Base):
    """
    Modelo de la tabla metodo_pago.
    Catálogo de métodos de pago disponibles.
    """
    __tablename__ = "metodo_pago"

    id_metodo_pago = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200))
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<MetodoPago(id={self.id_metodo_pago}, nombre='{self.nombre}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id_metodo_pago": self.id_metodo_pago,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo
        }