from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time
from decimal import Decimal


class DetalleComprobanteBase(BaseModel):
    numero_item: int
    codigo_producto: str = ""
    descripcion: str
    unidad: str = "NIU"
    cantidad: Decimal = Decimal("1.000")
    precio_unitario: Decimal
    precio_base: Decimal
    tipo_afectacion_igv: str = "10"
    porcentaje_igv: str = "18"
    igv: Decimal
    monto_descuento: Decimal = Decimal("0.00")
    importe_total: Decimal


class DetalleComprobanteCreate(DetalleComprobanteBase):
    pass


class DetalleComprobanteResponse(DetalleComprobanteBase):
    id: int
    comprobante_id: int
    
    class Config:
        from_attributes = True


class DocumentoReferenciaBase(BaseModel):
    tipo_documento: str
    serie: str
    correlativo: str
    motivo: str = ""


class DocumentoReferenciaCreate(DocumentoReferenciaBase):
    pass


class DocumentoReferenciaResponse(DocumentoReferenciaBase):
    id: int
    comprobante_id: int
    
    class Config:
        from_attributes = True


class ComprobanteBase(BaseModel):
    tipo_documento: str
    fecha_emision: date
    serie: str
    correlativo: str
    cliente_tipo_documento: str
    cliente_numero_documento: str
    cliente_denominacion: str
    cliente_direccion: str = ""
    importe_subtotal: Decimal
    importe_igv: Decimal
    importe_total: Decimal
    moneda: str = "PEN"
    observaciones: str = ""


class ComprobanteCreate(ComprobanteBase):
    empresa_id: int
    detalles: List[DetalleComprobanteCreate]
    referencias: List[DocumentoReferenciaBase] = []
    referencia_documento_id: Optional[int] = None
    referencia_motivo: str = ""


class ComprobanteUpdate(BaseModel):
    fecha_emision: Optional[date] = None
    cliente_tipo_documento: Optional[str] = None
    cliente_numero_documento: Optional[str] = None
    cliente_denominacion: Optional[str] = None
    observaciones: Optional[str] = None


class ComprobanteResponse(ComprobanteBase):
    id: int
    empresa_id: int
    numero: str
    xml_firmado: str = ""
    hash_cpe: str = ""
    cdr_sunat: str = ""
    codigo_respuesta: str = ""
    descripcion_respuesta: str = ""
    estado: str
    pdf_url: str = ""
    xml_url: str = ""
    cdr_url: str = ""
    referencia_documento_id: Optional[int] = None
    referencia_motivo: str = ""
    fecha_registro: datetime
    fecha_modificacion: datetime
    detalles: List[DetalleComprobanteResponse] = []
    
    class Config:
        from_attributes = True


class HistorialEnvioResponse(BaseModel):
    id: int
    comprobante_id: int
    fecha_envio: datetime
    tipo: str
    estado: str
    mensaje: str
    
    class Config:
        from_attributes = True