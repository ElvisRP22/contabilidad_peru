from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.models import Usuario
from app.core.schemas import (
    UsuarioCreate, UsuarioResponse, UsuarioUpdate,
    LoginRequest, Token, EmpresaCreate, EmpresaResponse, EmpresaUpdate,
    SerieDocumentoCreate, SerieDocumentoResponse
)
from app.auth.jwt import (
    create_access_token, create_refresh_token, decode_token,
    get_current_active_user
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == request.username).first()
    
    if not usuario or not usuario.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    access_token = create_access_token(data={"sub": usuario.id})
    refresh_token = create_refresh_token(data={"sub": usuario.id})
    
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh_token(request: dict, db: Session = Depends(get_db)):
    refresh_token = request.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="refresh_token es requerido"
        )
    payload = decode_token(refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de actualización inválido"
        )
    
    usuario_id = payload.get("sub")
    usuario = db.get(Usuario, usuario_id)
    
    if not usuario or not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )
    
    new_access_token = create_access_token(data={"sub": usuario.id})
    new_refresh_token = create_refresh_token(data={"sub": usuario.id})
    
    return Token(access_token=new_access_token, refresh_token=new_refresh_token)


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_active_user)):
    return current_user