from sqlalchemy.orm import Session
from app.repositories import citas_repository, pacientes_repository, doctores_repository
from app.schemas.cita import CitaCreate, CitaUpdate, CitaUpdateEstado
from fastapi import HTTPException

class CitaService:
    @staticmethod
    def crear_cita(db: Session, cita_data: CitaCreate):
        if not pacientes_repository.get_by_id(db, cita_data.id_paciente):
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        if not doctores_repository.get_by_id(db, cita_data.id_doctor):
            raise HTTPException(status_code=404, detail="Doctor no encontrado")
        if not citas_repository.verificar_disponibilidad(db, cita_data.id_doctor, cita_data.fecha, cita_data.hora):
            raise HTTPException(status_code=409, detail="El horario no está disponible")
        return citas_repository.create(db, cita_data)
    
    @staticmethod
    def obtener_cita(db: Session, cita_id: int):
        cita = citas_repository.get_by_id(db, cita_id)
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return cita
    
    @staticmethod
    def listar_citas(db: Session, skip: int = 0, limit: int = 100):
        return citas_repository.get_all(db, skip, limit)
    
    @staticmethod
    def actualizar_estado(db: Session, cita_id: int, estado: str):
        cita = citas_repository.get_by_id(db, cita_id)
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return citas_repository.update_estado(db, cita_id, estado)
    
    @staticmethod
    def cancelar_cita(db: Session, cita_id: int):
        cita = citas_repository.get_by_id(db, cita_id)
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return citas_repository.delete(db, cita_id)