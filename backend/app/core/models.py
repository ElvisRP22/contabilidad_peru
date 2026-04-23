from typing import Optional, List
from datetime import datetime, date, time
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Usuario(SQLModel, table=True):
    __tablename__ = "core_usuario"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: Optional[EmailStr] = None
    first_name: str = Field(default="")
    last_name: str = Field(default="")
    password: str = Field(default="")
    
    tipo_usuario: str = Field(default="cliente")
    empresa_id: Optional[int] = Field(default=None, foreign_key="core_empresa.id")
    telefono: str = Field(default="")
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    
    empresa: Optional["Empresa"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Usuario.empresa_id]"})
    
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Empresa(SQLModel, table=True):
    __tablename__ = "core_empresa"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    razon_social: str = Field(max_length=200)
    nombre_comercial: str = Field(default="")
    tipo_documento: str = Field(default="ruc")
    numero_documento: str = Field(max_length=20, unique=True)
    direccion: str = Field(default="")
    departamento: str = Field(default="")
    provincia: str = Field(default="")
    distrito: str = Field(default="")
    telefono: str = Field(default="")
    email: Optional[EmailStr] = None
    tipo_regimen: str = Field(default="general")
    representante_legal: str = Field(default="")
    dni_representante: str = Field(default="")
    
    certificado_digital: Optional[str] = None
    password_certificado: str = Field(default="")
    
    ose_enabled: bool = Field(default=False)
    ose_proveedor: str = Field(default="")
    ose_token: str = Field(default="")
    
    activa: bool = Field(default=True)
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    fecha_modificacion: datetime = Field(default_factory=datetime.utcnow)
    
    usuarios: List["Usuario"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Usuario.empresa_id]", "back_populates": "empresa"})
    series: List["SerieDocumento"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[SerieDocumento.empresa_id]", "back_populates": "empresa"})


class SerieDocumento(SQLModel, table=True):
    __tablename__ = "core_serie_documento"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    tipo_documento: str = Field(max_length=2)
    serie: str = Field(max_length=4)
    correlativo: int = Field(default=0)
    observaciones: str = Field(default="")
    
    empresa: "Empresa" = Relationship(sa_relationship_kwargs={"foreign_keys": "[SerieDocumento.empresa_id]", "back_populates": "series"})


class ParametroSistema(SQLModel, table=True):
    __tablename__ = "core_parametro"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    clave: str = Field(max_length=50)
    valor: str
    descripcion: str = Field(default="")