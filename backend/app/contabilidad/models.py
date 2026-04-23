from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship


class PlanCuenta(SQLModel, table=True):
    __tablename__ = "contabilidad_plan_cuenta"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    codigo: str = Field(max_length=10)
    nombre: str = Field(max_length=200)
    naturaleza: str
    tipo_cuenta: str
    nivel: int = Field(default=1)
    padre_id: Optional[int] = Field(default=None, foreign_key="contabilidad_plan_cuenta.id")
    acepta_movimiento: bool = Field(default=True)
    cta_banco: bool = Field(default=False)
    cta_efectivo: bool = Field(default=False)
    
    padre: Optional["PlanCuenta"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[PlanCuenta.padre_id]", "remote_side": "[PlanCuenta.id]"})
    hijos: List["PlanCuenta"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[PlanCuenta.padre_id]", "back_populates": "padre"})


class CentroCosto(SQLModel, table=True):
    __tablename__ = "contabilidad_centro_costo"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    codigo: str = Field(max_length=10)
    nombre: str = Field(max_length=100)
    activo: bool = Field(default=True)


class Asiento(SQLModel, table=True):
    __tablename__ = "contabilidad_asiento"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    numero: str = Field(max_length=20)
    fecha: date
    glosa: str = Field(default="")
    debe: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    haber: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    estado: str = Field(default="pendiente")
    cerrado: bool = Field(default=False)
    usuario_registra_id: Optional[int] = Field(default=None, foreign_key="core_usuario.id")
    usuario_aprueba_id: Optional[int] = Field(default=None, foreign_key="core_usuario.id")
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    fecha_aprueba: Optional[datetime] = None
    
    detalles: List["DetalleAsiento"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DetalleAsiento.asiento_id]", "back_populates": "asiento"})


class DetalleAsiento(SQLModel, table=True):
    __tablename__ = "contabilidad_detalle_asiento"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    asiento_id: int = Field(foreign_key="contabilidad_asiento.id")
    cuenta_id: int = Field(foreign_key="contabilidad_plan_cuenta.id")
    debe: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    haber: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    glosa: str = Field(default="")
    centro_costo_id: Optional[int] = Field(default=None, foreign_key="contabilidad_centro_costo.id")
    
    asiento: "Asiento" = Relationship(sa_relationship_kwargs={"foreign_keys": "[DetalleAsiento.asiento_id]", "back_populates": "detalles"})
    cuenta: "PlanCuenta" = Relationship(sa_relationship_kwargs={"foreign_keys": "[DetalleAsiento.cuenta_id]"})
    centro_costo: Optional["CentroCosto"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DetalleAsiento.centro_costo_id]"})