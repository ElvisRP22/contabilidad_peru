from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


class AlmacenBase(BaseModel):
    codigo: str
    nombre: str
    direccion: str = ""
    principal: bool = False
    activo: bool = True


class AlmacenCreate(AlmacenBase):
    empresa_id: int


class AlmacenResponse(AlmacenBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True


class CategoriaBase(BaseModel):
    codigo: str
    nombre: str
    padre_id: Optional[int] = None


class CategoriaCreate(CategoriaBase):
    empresa_id: int


class CategoriaResponse(CategoriaBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True


class ProductoBase(BaseModel):
    codigo: str
    codigo_barras: str = ""
    nombre: str
    descripcion: str = ""
    categoria_id: Optional[int] = None
    unidad: str = "NIU"
    presentacion: str = ""
    cantidad: Decimal = Decimal("0.000")
    cantidad_minima: Decimal = Decimal("0.000")
    cantidad_maxima: Decimal = Decimal("0.000")
    costo_unitario: Decimal = Decimal("0.00")
    precio_venta: Decimal = Decimal("0.00")
    permite_stock_negativo: bool = False
    activo: bool = True
    afecta_igv: bool = True
    tipo_afectacion: str = "10"


class ProductoCreate(ProductoBase):
    empresa_id: int


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    costo_unitario: Optional[Decimal] = None
    precio_venta: Optional[Decimal] = None
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True


class KardexBase(BaseModel):
    tipo_movimiento: str
    numero_documento: str = ""
    fecha_movimiento: date
    cantidad: Decimal
    costo_unitario: Decimal
    costo_total: Decimal
    cantidad_saldo: Decimal
    costo_promedio: Decimal
    costo_saldo: Decimal
    glosa: str = ""


class KardexCreate(KardexBase):
    empresa_id: int
    producto_id: int
    almacen_id: int


class KardexResponse(KardexBase):
    id: int
    empresa_id: int
    producto_id: int
    almacen_id: int
    referencia_id: Optional[int] = None
    referencia_tipo: str = ""
    usuario_registra_id: Optional[int] = None
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class StockAlmacenResponse(BaseModel):
    producto_id: int
    almacen_id: int
    cantidad: Decimal
    costo_promedio: Decimal
    
    class Config:
        from_attributes = True