from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select, func

from app.database import get_db
from app.core.models import Usuario, Empresa, SerieDocumento, ParametroSistema
from app.core.schemas import (
    UsuarioCreate, UsuarioResponse, UsuarioUpdate,
    EmpresaCreate, EmpresaResponse, EmpresaUpdate,
    SerieDocumentoCreate, SerieDocumentoResponse,
    ParametroSistemaCreate, ParametroSistemaResponse
)
from app.auth.jwt import get_current_active_user

router = APIRouter(prefix="/core", tags=["core"])


@router.get("/usuarios", response_model=list[UsuarioResponse])
def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Usuario).offset(skip).limit(limit)
    if current_user.tipo_usuario != "admin":
        query = query.where(Usuario.empresa_id == current_user.empresa_id)
    return db.exec(query).all()


@router.post("/usuarios", response_model=UsuarioResponse)
def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    existing = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username ya existe")
    
    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        first_name=usuario.first_name,
        last_name=usuario.last_name,
        tipo_usuario=usuario.tipo_usuario,
        empresa_id=usuario.empresa_id,
        telefono=usuario.telefono,
        password=Usuario.hash_password(usuario.password)
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = usuario_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = Usuario.hash_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/usuarios/{usuario_id}")
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuario eliminado"}


@router.get("/empresas", response_model=list[EmpresaResponse])
def list_empresas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = select(Empresa).offset(skip).limit(limit)
    if current_user.tipo_usuario == "cliente":
        query = query.where(Empresa.id == current_user.empresa_id)
    return db.exec(query).all()


@router.post("/empresas", response_model=EmpresaResponse)
def create_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    existing = db.query(Empresa).filter(Empresa.numero_documento == empresa.numero_documento).first()
    if existing:
        raise HTTPException(status_code=400, detail="Empresa ya existe")
    
    db_empresa = Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


@router.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
def get_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    empresa = db.get(Empresa, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.put("/empresas/{empresa_id}", response_model=EmpresaResponse)
def update_empresa(
    empresa_id: int,
    empresa_update: EmpresaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_empresa = db.get(Empresa, empresa_id)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    update_data = empresa_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


@router.get("/empresas/{empresa_id}/series", response_model=list[SerieDocumentoResponse])
def get_series(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    return db.exec(select(SerieDocumento).where(SerieDocumento.empresa_id == empresa_id)).all()


@router.post("/empresas/{empresa_id}/series", response_model=SerieDocumentoResponse)
def add_serie(
    empresa_id: int,
    serie: SerieDocumentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_serie = SerieDocumento(**serie.model_dump(), empresa_id=empresa_id)
    db.add(db_serie)
    db.commit()
    db.refresh(db_serie)
    return db_serie


@router.post("/empresas/{empresa_id}/agregar_serie", response_model=SerieDocumentoResponse)
def agregar_serie(
    empresa_id: int,
    serie: SerieDocumentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    return add_serie(empresa_id, serie, db, current_user)


@router.get("/parametros", response_model=list[ParametroSistemaResponse])
def list_parametros(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    return db.exec(select(ParametroSistema).where(ParametroSistema.empresa_id == empresa_id)).all()


@router.post("/parametros", response_model=ParametroSistemaResponse)
def create_parametro(
    parametro: ParametroSistemaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    db_parametro = ParametroSistema(**parametro.model_dump())
    db.add(db_parametro)
    db.commit()
    db.refresh(db_parametro)
    return db_parametro