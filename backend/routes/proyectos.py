from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.db.database import get_db
from backend.models.proyecto_model import Proyecto
from backend.schemas.proyecto_schema import ProyectoCreate, EstadoProyectoDBEnum
from backend.models.user_model import Usuario, RolEnum
from backend.models.postulacion_model import Postulacion
from backend.helpers.jwtAuth import verificar_token
from backend.models.carreras_model import Carrera

router = APIRouter()

# ruta para crear un proyecto
@router.post("/crear")
def crear_proyecto(proyecto_data: ProyectoCreate, usuario=Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario["sub"]).first()
    if not usuario_db or usuario_db.rol != RolEnum.estudiante:
        raise HTTPException(status_code=403, detail="Solo los estudiantes pueden crear proyectos")

    nuevo_proyecto = Proyecto(
        **proyecto_data.dict(exclude={"profesor_id", "perfiles_requeridos"}),
        creador_id=usuario_db.id,
        profesor_id=proyecto_data.profesor_id,
        perfiles_requeridos=[p.dict() for p in proyecto_data.perfiles_requeridos]
    )
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return {"mensaje": "proyecto creado con éxito"}

#ruta para ver todos mis proyectos creados
@router.get("/mis-proyectos")
def listar_proyectos_propios(usuario=Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario["sub"]).first()
    proyectos = db.query(Proyecto).filter(Proyecto.creador_id == usuario_db.id).all()
    return [
        {
            "id": p.id,
            "titulo": p.titulo,
            "resumen": p.resumen,
            "estado": p.estado.value
        }
        for p in proyectos
    ]

# ruta para postular a un proyecto
@router.post("/{proyecto_id}/postular")
def postular(proyecto_id: int, usuario=Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario["sub"]).first()
    if usuario_db.rol != RolEnum.estudiante:
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden postular")

    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if not proyecto or proyecto.creador_id == usuario_db.id:
        raise HTTPException(status_code=403, detail="No puedes postular a tu propio proyecto")

    if db.query(Postulacion).filter_by(proyecto_id=proyecto_id, usuario_id=usuario_db.id).first():
        raise HTTPException(status_code=400, detail="Ya postulaste")

    postulacion = Postulacion(proyecto_id=proyecto_id, usuario_id=usuario_db.id, estado="pendiente")
    db.add(postulacion)
    db.commit()
    return {"mensaje": "Postulación enviada con éxito"}

# ruta para ver postulaciones (solo el creador las puede ver)
@router.get("/{proyecto_id}/postulaciones")
def ver_postulaciones(proyecto_id: int, usuario=Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario["sub"]).first()
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if usuario_db.id != proyecto.creador_id:
        raise HTTPException(status_code=403, detail="Solo el creador puede ver las postulaciones")

    postulaciones = db.query(Postulacion).options(
        joinedload(Postulacion.estudiante).joinedload(Usuario.estudiante_info)
    ).filter_by(proyecto_id=proyecto_id).all()

    resultado = []
    for p in postulaciones:
        estudiante = p.estudiante
        estudiante_info = estudiante.estudiante_info
        carrera = None
        if estudiante_info:
            carrera_db = db.query(Carrera).filter_by(id=estudiante_info.carrera_id).first()
            if carrera_db:
                carrera = carrera_db.nombre

        resultado.append({
            "id": p.id,
            "estado": p.estado.value,
            "fecha_postulacion": p.fecha_postulacion,
            "usuario_id": estudiante.id,
            "nombre": estudiante.nombre,
            "apellido": estudiante.apellido,
            "carrera": carrera
        })

    return resultado

# ruta para aceptar o rechazar postulaciones
@router.patch("/{proyecto_id}/estado")
def cambiar_estado(proyecto_id: int, estado: EstadoProyectoDBEnum, usuario=Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario["sub"]).first()
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

    if proyecto.profesor_id != usuario_db.id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar el estado")

    proyecto.estado = estado
    db.commit()
    return {"mensaje": f"Proyecto marcado como {estado}"}

# ruta para ver los participantes de un proyecto
@router.get("/{proyecto_id}/integrantes")
def ver_integrantes(proyecto_id: int, usuario=Depends(verificar_token), db: Session = Depends(get_db)):
    proyecto = db.query(Proyecto).filter_by(id=proyecto_id).first()
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario["sub"]).first()

    if usuario_db.id not in [proyecto.creador_id, proyecto.profesor_id]:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    aceptados = db.query(Usuario).join(Postulacion).filter(
        Postulacion.proyecto_id == proyecto_id,
        Postulacion.estado == "aceptado"
    ).all()
    return aceptados


