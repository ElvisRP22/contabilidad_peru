from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from decimal import Decimal

from app.database import get_db
from app.core.models import Usuario
from app.inventario.models import Almacen, Categoria, Producto, Kardex, StockAlmacen
from app.inventario.schemas import (
    AlmacenCreate, AlmacenResponse,
    CategoriaCreate, CategoriaResponse,
    ProductoCreate, ProductoResponse, ProductoUpdate,
    KardexCreate, KardexResponse
)
from app.auth.jwt import get_current_active_user

router = APIRouter(prefix="/inventario", tags=["inventario"])


@router.get("/almacenes", response_model=list[AlmacenResponse])
def list_almacenes(
    empresa_id: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Almacen)
    if empresa_id:
        query = query.where(Almacen.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Almacen.empresa_id == current_user.empresa_id)
    return db.exec(query).all()


@router.post("/almacenes", response_model=AlmacenResponse)
def create_almacen(
    almacen: AlmacenCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_almacen = Almacen(**almacen.model_dump())
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen


@router.get("/categorias", response_model=list[CategoriaResponse])
def list_categorias(
    empresa_id: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Categoria)
    if empresa_id:
        query = query.where(Categoria.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Categoria.empresa_id == current_user.empresa_id)
    return db.exec(query).all()


@router.post("/categorias", response_model=CategoriaResponse)
def create_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_categoria = Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.get("/productos", response_model=list[ProductoResponse])
def list_productos(
    empresa_id: int = None,
    categoria_id: int = None,
    activo: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Producto)
    if empresa_id:
        query = query.where(Producto.empresa_id == empresa_id)
    elif current_user.tipo_usuario != "admin":
        query = query.where(Producto.empresa_id == current_user.empresa_id)
    if categoria_id:
        query = query.where(Producto.categoria_id == categoria_id)
    if activo is not None:
        query = query.where(Producto.activo == activo)
    return db.exec(query.offset(skip).limit(limit)).all()


@router.post("/productos", response_model=ProductoResponse)
def create_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.get("/productos/{producto_id}", response_model=ProductoResponse)
def get_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/productos/{producto_id}", response_model=ProductoResponse)
def update_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_producto = db.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.delete("/productos/{producto_id}")
def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_producto = db.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado"}


@router.get("/productos/{producto_id}/kardex", response_model=list[KardexResponse])
def get_kardex_producto(
    producto_id: int,
    desde: str = None,
    hasta: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Kardex).where(Kardex.producto_id == producto_id)
    if desde:
        query = query.where(Kardex.fecha_movimiento >= desde)
    if hasta:
        query = query.where(Kardex.fecha_movimiento <= hasta)
    return db.exec(query.order_by(Kardex.fecha_movimiento, Kardex.id)).all()


@router.post("/kardex", response_model=KardexResponse)
def create_kardex(
    kardex: KardexCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_kardex = Kardex(**kardex.model_dump(), usuario_registra_id=current_user.id)
    db.add(db_kardex)
    
    stock = db.exec(select(StockAlmacen).where(
        StockAlmacen.producto_id == kardex.producto_id,
        StockAlmacen.almacen_id == kardex.almacen_id
    )).first()
    
    if not stock:
        stock = StockAlmacen(
            producto_id=kardex.producto_id,
            almacen_id=kardex.almacen_id,
            cantidad=kardex.cantidad_saldo,
            costo_promedio=kardex.costo_promedio
        )
        db.add(stock)
    else:
        stock.cantidad = kardex.cantidad_saldo
        stock.costo_promedio = kardex.costo_promedio
    
    db.commit()
    db.refresh(db_kardex)
    return db_kardex


@router.get("/stock", response_model=list)
def get_stock(
    empresa_id: int,
    producto_id: int = None,
    almacen_id: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(StockAlmacen).join(Producto).where(Producto.empresa_id == empresa_id)
    if producto_id:
        query = query.where(StockAlmacen.producto_id == producto_id)
    if almacen_id:
        query = query.where(StockAlmacen.almacen_id == almacen_id)
    return db.exec(query).all()