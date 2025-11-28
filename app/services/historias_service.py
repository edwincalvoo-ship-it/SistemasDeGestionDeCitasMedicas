
from sqlalchemy.orm import Session
from app.repositories import historias_repository, pacientes_repository, doctores_repository, citas_repository
from app.schemas.historia import HistoriaCreate
from fastapi import HTTPException

class HistoriaService:
    @staticmethod
    def crear_historia(db: Session, historia_data: HistoriaCreate):
        if not pacientes_repository.get_by_id(db, historia_data.id_paciente):
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        if not doctores_repository.get_by_id(db, historia_data.id_doctor):
            raise HTTPException(status_code=404, detail="Doctor no encontrado")
        if historia_data.id_cita and not citas_repository.get_by_id(db, historia_data.id_cita):
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return historias_repository.create(db, historia_data)
    
    @staticmethod
    def obtener_historias_paciente(db: Session, paciente_id: int):
        if not pacientes_repository.get_by_id(db, paciente_id):
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return historias_repository.get_by_paciente(db, paciente_id)