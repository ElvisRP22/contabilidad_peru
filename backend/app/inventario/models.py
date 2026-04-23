from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship


class Almacen(SQLModel, table=True):
    __tablename__ = "inventario_almacen"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    codigo: str = Field(max_length=10)
    nombre: str = Field(max_length=100)
    direccion: str = Field(default="")
    principal: bool = Field(default=False)
    activo: bool = Field(default=True)


class Categoria(SQLModel, table=True):
    __tablename__ = "inventario_categoria"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    codigo: str = Field(max_length=10)
    nombre: str = Field(max_length=100)
    padre_id: Optional[int] = Field(default=None, foreign_key="inventario_categoria.id")
    
    padre: Optional["Categoria"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Categoria.padre_id]", "remote_side": "[Categoria.id]"})
    subcategorias: List["Categoria"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Categoria.padre_id]", "back_populates": "padre"})


class Producto(SQLModel, table=True):
    __tablename__ = "inventario_producto"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    codigo: str = Field(max_length=30)
    codigo_barras: str = Field(default="")
    nombre: str = Field(max_length=200)
    descripcion: str = Field(default="")
    
    categoria_id: Optional[int] = Field(default=None, foreign_key="inventario_categoria.id")
    unidad: str = Field(default="NIU")
    presentacion: str = Field(default="")
    
    cantidad: Decimal = Field(default=Decimal("0.000"), decimal_places=3, max_digits=15)
    cantidad_minima: Decimal = Field(default=Decimal("0.000"), decimal_places=3, max_digits=15)
    cantidad_maxima: Decimal = Field(default=Decimal("0.000"), decimal_places=3, max_digits=15)
    
    costo_unitario: Decimal = Field(default=Decimal("0.0000000000"), decimal_places=10, max_digits=15)
    precio_venta: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    
    permite_stock_negativo: bool = Field(default=False)
    activo: bool = Field(default=True)
    afecta_igv: bool = Field(default=True)
    tipo_afectacion: str = Field(default="10")


class Kardex(SQLModel, table=True):
    __tablename__ = "inventario_kardex"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    producto_id: int = Field(foreign_key="inventario_producto.id")
    almacen_id: int = Field(foreign_key="inventario_almacen.id")
    
    tipo_movimiento: str
    numero_documento: str = Field(default="")
    fecha_movimiento: date
    
    cantidad: Decimal = Field(decimal_places=3, max_digits=15)
    costo_unitario: Decimal = Field(decimal_places=10, max_digits=15)
    costo_total: Decimal = Field(decimal_places=2, max_digits=15)
    
    cantidad_saldo: Decimal = Field(decimal_places=3, max_digits=15)
    costo_promedio: Decimal = Field(decimal_places=10, max_digits=15)
    costo_saldo: Decimal = Field(decimal_places=2, max_digits=15)
    
    glosa: str = Field(default="")
    referencia_id: Optional[int] = None
    referencia_tipo: str = Field(default="")
    usuario_registra_id: Optional[int] = Field(default=None, foreign_key="core_usuario.id")
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)


class StockAlmacen(SQLModel, table=True):
    __tablename__ = "inventario_stock_almacen"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="inventario_producto.id")
    almacen_id: int = Field(foreign_key="inventario_almacen.id")
    cantidad: Decimal = Field(default=Decimal("0.000"), decimal_places=3, max_digits=15)
    costo_promedio: Decimal = Field(default=Decimal("0.0000000000"), decimal_places=10, max_digits=15)