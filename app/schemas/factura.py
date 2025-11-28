from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class FacturaCreate(BaseModel):
    id_cita: int = Field(..., gt=0)
    id_metodo_pago: int = Field(..., gt=0)
    monto: Decimal = Field(..., gt=0, decimal_places=2)
    observaciones: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id_cita": 1,
                "id_metodo_pago": 1,
                "monto": 50000.00,
                "observaciones": "Pago consulta médica"
            }
        }

class FacturaResponse(BaseModel):
    id_factura: int
    id_cita: int
    id_metodo_pago: int
    monto: Decimal
    fecha_emision: datetime
    estado: str
    observaciones: Optional[str]

    class Config:
        from_attributes = True