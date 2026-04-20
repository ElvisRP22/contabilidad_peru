from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


class UsuarioBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    first_name: str = ""
    last_name: str = ""
    tipo_usuario: str = "cliente"
    empresa_id: Optional[int] = None
    telefono: str = ""


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tipo_usuario: Optional[str] = None
    empresa_id: Optional[int] = None
    telefono: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    is_staff: bool
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    usuario_id: Optional[int] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class EmpresaBase(BaseModel):
    razon_social: str
    nombre_comercial: str = ""
    tipo_documento: str = "ruc"
    numero_documento: str
    direccion: str = ""
    departamento: str = ""
    provincia: str = ""
    distrito: str = ""
    telefono: str = ""
    email: Optional[EmailStr] = None
    tipo_regimen: str = "general"
    representante_legal: str = ""
    dni_representante: str = ""


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    razon_social: Optional[str] = None
    nombre_comercial: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo_regimen: Optional[str] = None
    activa: Optional[bool] = None


class EmpresaResponse(EmpresaBase):
    id: int
    activa: bool
    fecha_registro: datetime
    fecha_modificacion: datetime
    
    class Config:
        from_attributes = True


class SerieDocumentoBase(BaseModel):
    tipo_documento: str
    serie: str
    correlativo: int = 0
    observaciones: str = ""


class SerieDocumentoCreate(SerieDocumentoBase):
    empresa_id: int


class SerieDocumentoResponse(SerieDocumentoBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True


class ParametroSistemaBase(BaseModel):
    clave: str
    valor: str
    descripcion: str = ""


class ParametroSistemaCreate(ParametroSistemaBase):
    empresa_id: int


class ParametroSistemaResponse(ParametroSistemaBase):
    id: int
    empresa_id: int
    
    class Config:
        from_attributes = True