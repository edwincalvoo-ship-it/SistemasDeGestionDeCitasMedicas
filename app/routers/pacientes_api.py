"""
Router API para gestión de Pacientes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteResponse, PacienteListResponse
from app.services.pacientes_service import PacienteService

router = APIRouter(
    prefix="/api/pacientes",
    tags=["Pacientes"]
)

@router.post("/registrar", response_model=dict, status_code=status.HTTP_200_OK)
def registrar_paciente(
    paciente_data: PacienteCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar un nuevo paciente.
    
    - **nombre**: Nombre del paciente (requerido)
    - **apellido**: Apellido del paciente (requerido)
    - **documento**: Documento de identidad único (requerido)
    - **correo**: Correo electrónico único (requerido)
    - **telefono**: Número de teléfono (requerido)
    - **direccion**: Dirección de residencia (opcional)
    - **fecha_nacimiento**: Fecha de nacimiento en formato YYYY-MM-DD (requerido)
    
    Retorna información del paciente creado.
    """
    try:
        paciente = PacienteService.crear_paciente(db, paciente_data)
        
        return {
            "success": True,
            "mensaje": "Paciente registrado con éxito",
            "data": {
                "id_paciente": paciente.id_paciente,
                "nombre": f"{paciente.nombre} {paciente.apellido}",
                "documento": paciente.documento,
                "correo": paciente.correo
            }
        }
    except HTTPException as e:
        return {
            "success": False,
            "mensaje": e.detail,
            "error_code": e.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }

@router.get("", response_model=dict)
def listar_pacientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar todos los pacientes con paginación.
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Límite de registros a retornar (default: 100)
    """
    try:
        pacientes = PacienteService.obtener_todos_pacientes(db, skip, limit)
        
        pacientes_data = [
            {
                "id_paciente": p.id_paciente,
                "nombre": p.nombre,
                "apellido": p.apellido,
                "documento": p.documento,
                "correo": p.correo,
                "telefono": p.telefono
            }
            for p in pacientes
        ]
        
        return {
            "success": True,
            "mensaje": "Pacientes obtenidos con éxito",
            "data": pacientes_data
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }

@router.get("/{paciente_id}", response_model=dict)
def obtener_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener información de un paciente específico por ID.
    
    - **paciente_id**: ID del paciente
    """
    try:
        paciente = PacienteService.obtener_paciente_por_id(db, paciente_id)
        
        return {
            "success": True,
            "mensaje": "Paciente encontrado",
            "data": paciente.to_dict()
        }
    except HTTPException as e:
        return {
            "success": False,
            "mensaje": e.detail,
            "error_code": e.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }

@router.put("/{paciente_id}", response_model=dict)
def actualizar_paciente(
    paciente_id: int,
    paciente_data: PacienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar información de un paciente.
    
    - **paciente_id**: ID del paciente a actualizar
    
    Solo se actualizarán los campos proporcionados.
    """
    try:
        paciente = PacienteService.actualizar_paciente(db, paciente_id, paciente_data)
        
        return {
            "success": True,
            "mensaje": "Paciente actualizado con éxito",
            "data": paciente.to_dict()
        }
    except HTTPException as e:
        return {
            "success": False,
            "mensaje": e.detail,
            "error_code": e.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }

@router.delete("/{paciente_id}", response_model=dict)
def eliminar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un paciente del sistema.
    
    - **paciente_id**: ID del paciente a eliminar
    """
    try:
        PacienteService.eliminar_paciente(db, paciente_id)
        
        return {
            "success": True,
            "mensaje": "Paciente eliminado con éxito",
            "data": None
        }
    except HTTPException as e:
        return {
            "success": False,
            "mensaje": e.detail,
            "error_code": e.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }