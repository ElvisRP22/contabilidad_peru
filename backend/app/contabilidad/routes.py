from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select, func
from decimal import Decimal
from datetime import datetime

from app.database import get_db
from app.core.models import Usuario
from app.contabilidad.models import PlanCuenta, CentroCosto, Asiento, DetalleAsiento
from app.contabilidad.schemas import (
    PlanCuentaCreate, PlanCuentaResponse, PlanCuentaUpdate,
    CentroCostoCreate, CentroCostoResponse,
    AsientoCreate, AsientoResponse, DetalleAsientoCreate
)
from app.auth.jwt import get_current_active_user

router = APIRouter(prefix="/contabilidad", tags=["contabilidad"])


def get_empresa_filter(current_user: Usuario):
    if current_user.tipo_usuario == "admin":
        return None
    return current_user.empresa_id


@router.get("/plan-cuentas", response_model=list[PlanCuentaResponse])
def list_cuentas(
    empresa_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(PlanCuenta)
    if empresa_id:
        query = query.where(PlanCuenta.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(PlanCuenta.empresa_id == current_user.empresa_id)
    return db.exec(query.offset(skip).limit(limit)).all()


@router.post("/plan-cuentas", response_model=PlanCuentaResponse)
def create_cuenta(
    cuenta: PlanCuentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_cuenta = PlanCuenta(**cuenta.model_dump())
    db.add(db_cuenta)
    db.commit()
    db.refresh(db_cuenta)
    return db_cuenta


@router.get("/plan-cuentas/{cuenta_id}", response_model=PlanCuentaResponse)
def get_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    cuenta = db.get(PlanCuenta, cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta


@router.put("/plan-cuentas/{cuenta_id}", response_model=PlanCuentaResponse)
def update_cuenta(
    cuenta_id: int,
    cuenta_update: PlanCuentaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_cuenta = db.get(PlanCuenta, cuenta_id)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    update_data = cuenta_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cuenta, key, value)
    
    db.commit()
    db.refresh(db_cuenta)
    return db_cuenta


@router.delete("/plan-cuentas/{cuenta_id}")
def delete_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_cuenta = db.get(PlanCuenta, cuenta_id)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    db.delete(db_cuenta)
    db.commit()
    return {"message": "Cuenta eliminada"}


@router.get("/centros-costo", response_model=list[CentroCostoResponse])
def list_centros(
    empresa_id: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(CentroCosto)
    if empresa_id:
        query = query.where(CentroCosto.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(CentroCosto.empresa_id == current_user.empresa_id)
    return db.exec(query).all()


@router.post("/centros-costo", response_model=CentroCostoResponse)
def create_centro(
    centro: CentroCostoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_centro = CentroCosto(**centro.model_dump())
    db.add(db_centro)
    db.commit()
    db.refresh(db_centro)
    return db_centro


@router.get("/asientos", response_model=list[AsientoResponse])
def list_asientos(
    empresa_id: int = None,
    fecha: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Asiento)
    if empresa_id:
        query = query.where(Asiento.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Asiento.empresa_id == current_user.empresa_id)
    return db.exec(query.offset(skip).limit(limit)).all()


@router.post("/asientos", response_model=AsientoResponse)
def create_asiento(
    asiento: AsientoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    debe_total = sum(d.debe for d in asiento.detalles)
    haber_total = sum(d.haber for d in asiento.detalles)
    
    if debe_total != haber_total:
        raise HTTPException(
            status_code=400,
            detail=f"Partida doble no balancea: Debe {debe_total} != Haber {haber_total}"
        )
    
    db_asiento = Asiento(
        empresa_id=asiento.empresa_id,
        numero=asiento.numero,
        fecha=asiento.fecha,
        glosa=asiento.glosa,
        debe=debe_total,
        haber=haber_total,
        usuario_registra_id=current_user.id
    )
    db.add(db_asiento)
    db.flush()
    
    for det in asiento.detalles:
        db_detalle = DetalleAsiento(
            asiento_id=db_asiento.id,
            cuenta_id=det.cuenta_id,
            debe=det.debe,
            haber=det.haber,
            glosa=det.glosa,
            centro_costo_id=det.centro_costo_id
        )
        db.add(db_detalle)
    
    db.commit()
    db.refresh(db_asiento)
    return db_asiento


@router.get("/asientos/{asiento_id}", response_model=AsientoResponse)
def get_asiento(
    asiento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    asiento = db.get(Asiento, asiento_id)
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    return asiento


@router.post("/asientos/{asiento_id}/aprobar")
def aprobar_asiento(
    asiento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    asiento = db.get(Asiento, asiento_id)
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    if asiento.estado == "aprobado":
        raise HTTPException(status_code=400, detail="Asiento ya aprobado")
    
    asiento.estado = "aprobado"
    asiento.usuario_aprueba_id = current_user.id
    asiento.fecha_aprueba = datetime.utcnow()
    db.commit()
    return {"message": "Asiento aprobado"}


@router.post("/asientos/{asiento_id}/cerrar")
def cerrar_asiento(
    asiento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    asiento = db.get(Asiento, asiento_id)
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    if asiento.cerrado:
        raise HTTPException(status_code=400, detail="Asiento ya cerrado")
    
    asiento.cerrado = True
    db.commit()
    return {"message": "Asiento cerrado"}


@router.get("/reportes/balance_comprobacion")
def balance_comprobacion(
    empresa_id: int,
    fecha: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = """
        SELECT 
            pc.codigo as cuenta_codigo,
            pc.nombre as cuenta_nombre,
            pc.naturaleza,
            COALESCE(SUM(da.debe), 0) as debe,
            COALESCE(SUM(da.haber), 0) as haber
        FROM contabilidad_plan_cuenta pc
        LEFT JOIN contabilidad_detalle_asiento da ON pc.id = da.cuenta_id
        LEFT JOIN contabilidad_asiento a ON da.asiento_id = a.id
        WHERE pc.empresa_id = :empresa_id 
            AND pc.acepta_movimiento = true
            AND a.fecha <= :fecha
            AND a.cerrado = true
        GROUP BY pc.id, pc.codigo, pc.nombre, pc.naturaleza
        ORDER BY pc.codigo
    """
    result = db.exec(query, {"empresa_id": empresa_id, "fecha": fecha}).all()
    
    balances = []
    for row in result:
        saldo_deudor = row.debe - row.haber if row.naturaleza == "deudora" else 0
        saldo_acreedor = row.haber - row.debe if row.naturaleza == "acreedora" else 0
        balances.append({
            "cuenta_codigo": row.cuenta_codigo,
            "cuenta_nombre": row.cuenta_nombre,
            "naturaleza": row.naturaleza,
            "debe": row.debe,
            "haber": row.haber,
            "saldo_deudor": saldo_deudor if saldo_deudor > 0 else 0,
            "saldo_acreedor": saldo_acreedor if saldo_acreedor > 0 else 0
        })
    return balances


@router.get("/reportes/mayor")
def mayor(
    empresa_id: int,
    cuenta_id: int,
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    detalles = db.exec(select(DetalleAsiento).join(Asiento).where(
        DetalleAsiento.cuenta_id == cuenta_id,
        Asiento.empresa_id == empresa_id,
        Asiento.fecha >= fecha_inicio,
        Asiento.fecha <= fecha_fin,
        Asiento.cerrado == True
    )).all()
    
    saldo = Decimal("0.00")
    movimientos = []
    for d in detalles:
        saldo += d.debe - d.haber
        movimientos.append({
            "fecha": d.asiento.fecha,
            "numero": d.asiento.numero,
            "glosa": d.glosa,
            "debe": d.debe,
            "haber": d.haber,
            "saldo": saldo
        })
    return movimientos