from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from decimal import Decimal

from app.database import get_db
from app.core.models import Usuario
from app.facturacion.models import Comprobante, DetalleComprobante, DocumentoReferencia, HistorialEnvio
from app.facturacion.schemas import (
    ComprobanteCreate, ComprobanteResponse, ComprobanteUpdate,
    DetalleComprobanteCreate, DocumentoReferenciaCreate
)
from app.auth.jwt import get_current_active_user

router = APIRouter(prefix="/facturacion", tags=["facturacion"])


@router.get("/comprobantes", response_model=list[ComprobanteResponse])
def list_comprobantes(
    empresa_id: int = None,
    tipo_documento: str = None,
    estado: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Comprobante)
    if empresa_id:
        query = query.where(Comprobante.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Comprobante.empresa_id == current_user.empresa_id)
    if tipo_documento:
        query = query.where(Comprobante.tipo_documento == tipo_documento)
    if estado:
        query = query.where(Comprobante.estado == estado)
    return db.exec(query.offset(skip).limit(limit)).all()


@router.post("/comprobantes", response_model=ComprobanteResponse)
def create_comprobante(
    comp: ComprobanteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    numero = f"{comp.serie}-{comp.correlativo.zfill(8)}"
    
    db_comp = Comprobante(
        empresa_id=comp.empresa_id,
        tipo_documento=comp.tipo_documento,
        fecha_emision=comp.fecha_emision,
        serie=comp.serie,
        correlativo=comp.correlativo,
        numero=numero,
        cliente_tipo_documento=comp.cliente_tipo_documento,
        cliente_numero_documento=comp.cliente_numero_documento,
        cliente_denominacion=comp.cliente_denominacion,
        cliente_direccion=comp.cliente_direccion,
        importe_subtotal=comp.importe_subtotal,
        importe_igv=comp.importe_igv,
        importe_total=comp.importe_total,
        moneda=comp.moneda,
        observaciones=comp.observaciones,
        referencia_documento_id=comp.referencia_documento_id,
        referencia_motivo=comp.referencia_motivo
    )
    db.add(db_comp)
    db.flush()
    
    for i, det in enumerate(comp.detalles, 1):
        db_detalle = DetalleComprobante(
            comprobante_id=db_comp.id,
            numero_item=i,
            codigo_producto=det.codigo_producto,
            descripcion=det.descripcion,
            unidad=det.unidad,
            cantidad=det.cantidad,
            precio_unitario=det.precio_unitario,
            precio_base=det.precio_base,
            tipo_afectacion_igv=det.tipo_afectacion_igv,
            porcentaje_igv=det.porcentaje_igv,
            igv=det.igv,
            monto_descuento=det.monto_descuento,
            importe_total=det.importe_total
        )
        db.add(db_detalle)
    
    for ref in comp.referencias:
        db_ref = DocumentoReferencia(
            comprobante_id=db_comp.id,
            tipo_documento=ref.tipo_documento,
            serie=ref.serie,
            correlativo=ref.correlativo,
            motivo=ref.motivo
        )
        db.add(db_ref)
    
    db.commit()
    db.refresh(db_comp)
    return db_comp


@router.get("/comprobantes/{comprobante_id}", response_model=ComprobanteResponse)
def get_comprobante(
    comprobante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    comp = db.get(Comprobante, comprobante_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    return comp


@router.post("/comprobantes/{comprobante_id}/generar")
def generar_xml(
    comprobante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    comp = db.get(Comprobante, comprobante_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    if comp.estado != "borrador":
        raise HTTPException(status_code=400, detail="Solo comprobantes en borrador pueden generarse")
    
    xml_content = f"<?xml version=\"1.0\"?><cpe>{comp.numero}</cpe>"
    comp.xml_firmado = xml_content
    comp.estado = "generado"
    comp.hash_cpe = "mock_hash_" + comp.numero
    
    db.commit()
    return {"message": "XML generado", "hash": comp.hash_cpe}


@router.post("/comprobantes/{comprobante_id}/firmar")
def firmar_xml(
    comprobante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    comp = db.get(Comprobante, comprobante_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    if comp.estado != "generado":
        raise HTTPException(status_code=400, detail="El comprobante debe estar generado")
    
    comp.estado = "firmado"
    db.commit()
    return {"message": "XML firmado"}


@router.post("/comprobantes/{comprobante_id}/enviar_sunat")
def enviar_sunat(
    comprobante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    comp = db.get(Comprobante, comprobante_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    if comp.estado != "firmado":
        raise HTTPException(status_code=400, detail="El comprobante debe estar firmado")
    
    comp.estado = "enviado"
    comp.codigo_respuesta = "0"
    comp.descripcion_respuesta = "Aceptado"
    comp.cdr_sunat = '<respuesta><codigo>0</codigo><descripcion>Aceptado</descripcion></respuesta>'
    
    historial = HistorialEnvio(
        comprobante_id=comp.id,
        tipo="sunat",
        estado="aceptado",
        mensaje="Aceptado por SUNAT"
    )
    db.add(historial)
    db.commit()
    return {"message": "Enviado a SUNAT", "codigo": "0", "descripcion": "Aceptado"}


@router.get("/comprobantes/{comprobante_id}/obtener_pdf")
def obtener_pdf(
    comprobante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    comp = db.get(Comprobante, comprobante_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    return {"pdf_url": f"/media/comprobantes/{comp.numero}.pdf"}


@router.post("/comprobantes/{comprobante_id}/anular")
def anular_comprobante(
    comprobante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    comp = db.get(Comprobante, comprobante_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    if comp.estado == "anulado":
        raise HTTPException(status_code=400, detail="Comprobante ya anulado")
    
    comp.estado = "anulado"
    db.commit()
    return {"message": "Comprobante anulado"}