from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from decimal import Decimal

from app.database import get_db
from app.core.models import Usuario
from app.nomina.models import Empleado, Remuneracion, Descuento, BeneficioSocial, Asistencia, Planilla
from app.nomina.schemas import (
    EmpleadoCreate, EmpleadoResponse, EmpleadoUpdate,
    RemuneracionCreate, DescuentoCreate,
    BeneficioSocialCreate, AsistenciaCreate, PlanillaCreate, PlanillaResponse
)
from app.auth.jwt import get_current_active_user

router = APIRouter(prefix="/nomina", tags=["nomina"])


@router.get("/empleados", response_model=list[EmpleadoResponse])
def list_empleados(
    empresa_id: int = None,
    activo: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Empleado)
    if empresa_id:
        query = query.where(Empleado.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Empleado.empresa_id == current_user.empresa_id)
    if activo is not None:
        query = query.where(Empleado.activo == activo)
    return db.exec(query.offset(skip).limit(limit)).all()


@router.post("/empleados", response_model=EmpleadoResponse)
def create_empleado(
    empleado: EmpleadoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    existing = db.exec(select(Empleado).where(
        Empleado.empresa_id == empleado.empresa_id,
        Empleado.numero_documento == empleado.numero_documento
    )).first()
    if existing:
        raise HTTPException(status_code=400, detail="Empleado ya existe")
    
    db_empleado = Empleado(**empleado.model_dump())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado


@router.get("/empleados/{empleado_id}", response_model=EmpleadoResponse)
def get_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    empleado = db.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.put("/empleados/{empleado_id}", response_model=EmpleadoResponse)
def update_empleado(
    empleado_id: int,
    empleado_update: EmpleadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_empleado = db.get(Empleado, empleado_id)
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    update_data = empleado_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_empleado, key, value)
    
    db.commit()
    db.refresh(db_empleado)
    return db_empleado


@router.delete("/empleados/{empleado_id}")
def delete_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_empleado = db.get(Empleado, empleado_id)
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    db.delete(db_empleado)
    db.commit()
    return {"message": "Empleado eliminado"}


@router.get("/empleados/{empleado_id}/remuneraciones")
def get_remuneraciones(
    empleado_id: int,
    periodo: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Remuneracion).where(Remuneracion.empleado_id == empleado_id)
    if periodo:
        query = query.where(Remuneracion.periodo == periodo)
    return db.exec(query).all()


@router.get("/empleados/{empleado_id}/descuentos")
def get_descuentos(
    empleado_id: int,
    periodo: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Descuento).where(Descuento.empleado_id == empleado_id)
    if periodo:
        query = query.where(Descuento.periodo == periodo)
    return db.exec(query).all()


@router.post("/remuneraciones", response_model=dict)
def create_remuneracion(
    remuneracion: RemuneracionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_rem = Remuneracion(**remuneracion.model_dump())
    db.add(db_rem)
    db.commit()
    return {"message": "Remuneración creada"}


@router.post("/descuentos", response_model=dict)
def create_descuento(
    descuento: DescuentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_desc = Descuento(**descuento.model_dump())
    db.add(db_desc)
    db.commit()
    return {"message": "Descuento creado"}


@router.get("/planillas", response_model=list[PlanillaResponse])
def list_planillas(
    empresa_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Planilla)
    if empresa_id:
        query = query.where(Planilla.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Planilla.empresa_id == current_user.empresa_id)
    return db.exec(query.offset(skip).limit(limit)).all()


@router.post("/planillas", response_model=PlanillaResponse)
def create_planilla(
    planilla: PlanillaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_planilla = Planilla(**planilla.model_dump())
    db.add(db_planilla)
    db.commit()
    db.refresh(db_planilla)
    return db_planilla


@router.get("/planillas/{planilla_id}", response_model=PlanillaResponse)
def get_planilla(
    planilla_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    planilla = db.get(Planilla, planilla_id)
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    return planilla


@router.post("/planillas/{planilla_id}/generar_planilla")
def generar_planilla(
    planilla_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    planilla = db.get(Planilla, planilla_id)
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    
    empleados = db.exec(select(Empleado).where(
        Empleado.empresa_id == planilla.empresa_id,
        Empleado.activo == True
    )).all()
    
    total_ingresos = Decimal("0.00")
    total_descuentos = Decimal("0.00")
    total_neto = Decimal("0.00")
    
    for emp in empleados:
        basic = Decimal("1025.00")
        total_ingresos += basic
        total_neto += basic
    
    planilla.total_empleados = len(empleados)
    planilla.total_ingresos = total_ingresos
    planilla.total_descuentos = total_descuentos
    planilla.total_neto = total_neto
    db.commit()
    
    return {"message": "Planilla generada", "total_empleados": len(empleados)}


@router.get("/planillas/{planilla_id}/generar_plame")
def generar_plame(
    planilla_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    planilla = db.get(Planilla, planilla_id)
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    
    return {
        "message": "PLAME generado",
        "periodo": planilla.periodo,
        "archivo": f"/media/planillas/plame_{planilla.periodo}.txt"
    }


@router.get("/beneficios", response_model=list)
def list_beneficios(
    empleado_id: int = None,
    tipo: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(BeneficioSocial)
    if empleado_id:
        query = query.where(BeneficioSocial.empleado_id == empleado_id)
    if tipo:
        query = query.where(BeneficioSocial.tipo == tipo)
    return db.exec(query).all()


@router.post("/beneficios", response_model=dict)
def create_beneficio(
    beneficio: BeneficioSocialCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_beneficio = BeneficioSocial(**beneficio.model_dump())
    db.add(db_beneficio)
    db.commit()
    return {"message": "Beneficio creado"}


@router.get("/asistencias", response_model=list)
def list_asistencias(
    empresa_id: int,
    empleado_id: int = None,
    fecha: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Asistencia).where(Asistencia.empresa_id == empresa_id)
    if empleado_id:
        query = query.where(Asistencia.empleado_id == empleado_id)
    if fecha:
        query = query.where(Asistencia.fecha == fecha)
    return db.exec(query).all()


@router.post("/asistencias", response_model=dict)
def create_asistencia(
    asistencia: AsistenciaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_asistencia = Asistencia(**asistencia.model_dump())
    db.add(db_asistencia)
    db.commit()
    return {"message": "Asistencia registrada"}