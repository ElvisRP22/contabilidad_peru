from typing import Optional, List
from datetime import datetime, date, time
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship


class Comprobante(SQLModel, table=True):
    __tablename__ = "facturacion_comprobante"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    tipo_documento: str
    moneda: str = Field(default="PEN")
    tipo_cambio: Decimal = Field(default=Decimal("1.000"), decimal_places=3, max_digits=10)
    fecha_emision: date
    hora_emision: Optional[time] = None
    
    serie: str = Field(max_length=4)
    correlativo: str = Field(max_length=8)
    numero: str = Field(max_length=13, unique=True)
    
    cliente_tipo_documento: str = Field(max_length=2)
    cliente_numero_documento: str = Field(max_length=20)
    cliente_denominacion: str = Field(max_length=200)
    cliente_direccion: str = Field(default="")
    
    importe_subtotal: Decimal = Field(decimal_places=2, max_digits=15)
    importe_igv: Decimal = Field(decimal_places=2, max_digits=15)
    importe_total: Decimal = Field(decimal_places=2, max_digits=15)
    
    formato: str = Field(default="json")
    observaciones: str = Field(default="")
    
    xml_firmado: str = Field(default="")
    hash_cpe: str = Field(default="")
    cdr_sunat: str = Field(default="")
    codigo_respuesta: str = Field(default="")
    descripcion_respuesta: str = Field(default="")
    
    estado: str = Field(default="borrador")
    pdf_url: str = Field(default="")
    xml_url: str = Field(default="")
    cdr_url: str = Field(default="")
    
    referencia_documento_id: Optional[int] = Field(default=None, foreign_key="facturacion_comprobante.id")
    referencia_motivo: str = Field(default="")
    
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    fecha_modificacion: datetime = Field(default_factory=datetime.utcnow)
    
    detalles: List["DetalleComprobante"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DetalleComprobante.comprobante_id]", "back_populates": "comprobante"})
    referencias: List["DocumentoReferencia"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DocumentoReferencia.comprobante_id]", "back_populates": "comprobante"})


class DetalleComprobante(SQLModel, table=True):
    __tablename__ = "facturacion_detalle_comprobante"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    comprobante_id: int = Field(foreign_key="facturacion_comprobante.id")
    numero_item: int
    
    codigo_producto: str = Field(default="")
    descripcion: str
    
    unidad: str = Field(default="NIU")
    cantidad: Decimal = Field(default=Decimal("1.000"), decimal_places=3, max_digits=15)
    
    precio_unitario: Decimal = Field(decimal_places=10, max_digits=15)
    precio_base: Decimal = Field(decimal_places=2, max_digits=15)
    
    tipo_afectacion_igv: str = Field(default="10")
    porcentaje_igv: str = Field(default="18")
    igv: Decimal = Field(decimal_places=2, max_digits=15)
    
    monto_descuento: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    importe_total: Decimal = Field(decimal_places=2, max_digits=15)
    
    comprobante: "Comprobante" = Relationship(sa_relationship_kwargs={"foreign_keys": "[DetalleComprobante.comprobante_id]", "back_populates": "detalles"})


class DocumentoReferencia(SQLModel, table=True):
    __tablename__ = "facturacion_documento_referencia"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    comprobante_id: int = Field(foreign_key="facturacion_comprobante.id")
    tipo_documento: str = Field(max_length=2)
    serie: str = Field(max_length=4)
    correlativo: str = Field(max_length=8)
    motivo: str = Field(default="")
    
    comprobante: "Comprobante" = Relationship(sa_relationship_kwargs={"foreign_keys": "[DocumentoReferencia.comprobante_id]", "back_populates": "referencias"})


class HistorialEnvio(SQLModel, table=True):
    __tablename__ = "facturacion_historial_envio"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    comprobante_id: int = Field(foreign_key="facturacion_comprobante.id")
    fecha_envio: datetime = Field(default_factory=datetime.utcnow)
    tipo: str = Field(max_length=20)
    request_data: str = Field(default="")
    response_data: str = Field(default="")
    estado: str = Field(max_length=20)
    mensaje: str = Field(default="")