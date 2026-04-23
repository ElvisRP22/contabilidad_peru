from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


class PlanCuentaBase(BaseModel):
    codigo: str
    nombre: str
    naturaleza: str
    tipo_cuenta: str
    nivel: int = 1
    padre_id: Optional[int] = None
    acepta_movimiento: bool = True
    cta_banco: bool = False
    cta_efectivo: bool = False


class PlanCuentaCreate(PlanCuentaBase):
    empresa_id: int


class PlanCuentaUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    naturaleza: Optional[str] = None
    tipo_cuenta: Optional[str] = None
    acepta_movimiento: Optional[bool] = None
    cta_banco: Optional[bool] = None
    cta_efectivo: Optional[bool] = None


class PlanCuentaResponse(PlanCuentaBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True


class CentroCostoBase(BaseModel):
    codigo: str
    nombre: str
    activo: bool = True


class CentroCostoCreate(CentroCostoBase):
    empresa_id: int


class CentroCostoResponse(CentroCostoBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True


class DetalleAsientoBase(BaseModel):
    cuenta_id: int
    debe: Decimal = Decimal("0.00")
    haber: Decimal = Decimal("0.00")
    glosa: str = ""
    centro_costo_id: Optional[int] = None


class DetalleAsientoCreate(DetalleAsientoBase):
    pass


class DetalleAsientoResponse(DetalleAsientoBase):
    id: int
    asiento_id: int
    
    class Config:
        from_attributes = True


class AsientoBase(BaseModel):
    numero: str
    fecha: date
    glosa: str = ""


class AsientoCreate(AsientoBase):
    empresa_id: int
    detalles: List[DetalleAsientoCreate]


class AsientoUpdate(BaseModel):
    numero: Optional[str] = None
    fecha: Optional[date] = None
    glosa: Optional[str] = None


class AsientoResponse(AsientoBase):
    id: int
    empresa_id: int
    debe: Decimal
    haber: Decimal
    estado: str
    cerrado: bool
    usuario_registra_id: Optional[int] = None
    usuario_aprueba_id: Optional[int] = None
    fecha_registro: datetime
    fecha_aprueba: Optional[datetime] = None
    detalles: List[DetalleAsientoResponse] = []
    
    class Config:
        from_attributes = True


class BalanceComprobacionResponse(BaseModel):
    cuenta_codigo: str
    cuenta_nombre: str
    naturaleza: str
    debe: Decimal
    haber: Decimal
    saldo_deudor: Decimal
    saldo_acreedor: Decimal