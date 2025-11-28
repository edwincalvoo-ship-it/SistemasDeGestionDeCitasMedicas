"""
Router API para gestión de Doctores
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse, EspecialidadResponse
from app.services.doctores_service import DoctorService
from app.dependencies.auth import require_admin, require_any_authenticated

router = APIRouter(
    prefix="/api/doctores",
    tags=["Doctores"]
)

@router.post("", response_model=dict, status_code=status.HTTP_200_OK)
def registrar_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    [HU-002] Endpoint para registrar un nuevo doctor (requiere rol admin).
    
    - **nombre**: Nombre del doctor (requerido)
    - **apellido**: Apellido del doctor (requerido)
    - **documento**: Documento de identidad único (requerido)
    - **correo**: Correo electrónico único (requerido)
    - **telefono**: Número de teléfono (opcional)
    - **licencia**: Licencia médica única (requerido)
    - **id_especialidad**: ID de la especialidad médica (requerido)
    
    Retorna información del doctor creado.
    """
    try:
        doctor = DoctorService.crear_doctor(db, doctor_data)
        
        return {
            "success": True,
            "mensaje": "Doctor registrado con éxito",
            "data": {
                "id_doctor": doctor.id_doctor,
                "nombre": f"{doctor.nombre} {doctor.apellido}",
                "especialidad": doctor.especialidad.nombre if doctor.especialidad else None,
                "licencia": doctor.licencia
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
def listar_doctores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar todos los doctores con paginación.
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Límite de registros a retornar (default: 100)
    """
    try:
        doctores = DoctorService.obtener_todos_doctores(db, skip, limit)
        
        doctores_data = [
            {
                "id_doctor": d.id_doctor,
                "nombre": d.nombre,
                "apellido": d.apellido,
                "documento": d.documento,
                "correo": d.correo,
                "telefono": d.telefono,
                "licencia": d.licencia,
                "especialidad": d.especialidad.nombre if d.especialidad else None,
                "activo": d.activo
            }
            for d in doctores
        ]
        
        return {
            "success": True,
            "mensaje": "Doctores obtenidos con éxito",
            "data": doctores_data
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }

@router.get("/{doctor_id}", response_model=dict)
def obtener_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener información de un doctor específico por ID.
    
    - **doctor_id**: ID del doctor
    """
    try:
        doctor = DoctorService.obtener_doctor_por_id(db, doctor_id)
        
        doctor_data = {
            "id_doctor": doctor.id_doctor,
            "nombre": doctor.nombre,
            "apellido": doctor.apellido,
            "documento": doctor.documento,
            "correo": doctor.correo,
            "telefono": doctor.telefono,
            "licencia": doctor.licencia,
            "id_especialidad": doctor.id_especialidad,
            "especialidad": {
                "id_especialidad": doctor.especialidad.id_especialidad,
                "nombre": doctor.especialidad.nombre,
                "descripcion": doctor.especialidad.descripcion
            } if doctor.especialidad else None,
            "activo": doctor.activo
        }
        
        return {
            "success": True,
            "mensaje": "Doctor encontrado",
            "data": doctor_data
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

@router.put("/{doctor_id}", response_model=dict)
def actualizar_doctor(
    doctor_id: int,
    doctor_data: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Endpoint para actualizar información de un doctor (requiere rol admin).
    
    - **doctor_id**: ID del doctor a actualizar
    
    Solo se actualizarán los campos proporcionados.
    """
    try:
        doctor = DoctorService.actualizar_doctor(db, doctor_id, doctor_data)
        
        return {
            "success": True,
            "mensaje": "Doctor actualizado con éxito",
            "data": {
                "id_doctor": doctor.id_doctor,
                "nombre": f"{doctor.nombre} {doctor.apellido}",
                "correo": doctor.correo,
                "especialidad": doctor.especialidad.nombre if doctor.especialidad else None
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

@router.delete("/{doctor_id}", response_model=dict)
def eliminar_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Endpoint para eliminar un doctor del sistema (requiere rol admin).
    
    - **doctor_id**: ID del doctor a eliminar
    """
    try:
        DoctorService.eliminar_doctor(db, doctor_id)
        
        return {
            "success": True,
            "mensaje": "Doctor eliminado con éxito",
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

# Endpoint adicional para listar especialidades
@router.get("/especialidades/listar", response_model=dict)
def listar_especialidades(db: Session = Depends(get_db)):
    """
    Endpoint para listar todas las especialidades médicas disponibles.
    """
    try:
        especialidades = DoctorService.obtener_especialidades(db)
        
        especialidades_data = [
            {
                "id_especialidad": e.id_especialidad,
                "nombre": e.nombre,
                "descripcion": e.descripcion
            }
            for e in especialidades
        ]
        
        return {
            "success": True,
            "mensaje": "Especialidades obtenidas con éxito",
            "data": especialidades_data
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Error interno en el servidor. Intente nuevamente más tarde.",
            "error_code": 500
        }