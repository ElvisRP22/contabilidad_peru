from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


class EmpleadoBase(BaseModel):
    numero_documento: str
    tipo_documento: str = "1"
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    sexo: str
    fecha_nacimiento: Optional[date] = None
    direccion: str = ""
    telefono: str = ""
    email: Optional[str] = None
    fecha_ingreso: date
    fecha_cese: Optional[date] = None
    motivo_cese: str = ""
    cargo: str = ""
    area: str = ""
    regimen_laboral: str = "General"
    jornada_trabajo: int = 8
    tipo_contrato: str = "Indeterminado"
    sindicate: bool = False
    cuenta_banco: str = ""
    banco: str = ""
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    empresa_id: int


class EmpleadoUpdate(BaseModel):
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    cargo: Optional[str] = None
    area: Optional[str] = None
    activo: Optional[bool] = None
    fecha_cese: Optional[date] = None
    motivo_cese: Optional[str] = None


class EmpleadoResponse(EmpleadoBase):
    id: int
    empresa_id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class RemuneracionBase(BaseModel):
    periodo: str
    basic_salary: Decimal
    asig_familiar: Decimal = Decimal("0.00")
    bonificacion: Decimal = Decimal("0.00")
    comision: Decimal = Decimal("0.00")
    overtime: Decimal = Decimal("0.00")
    otros: Decimal = Decimal("0.00")
    ingreso_gravado: Decimal = Decimal("0.00")
    ingreso_no_gravado: Decimal = Decimal("0.00")
    total_ingreso: Decimal = Decimal("0.00")


class RemuneracionCreate(RemuneracionBase):
    empleado_id: int


class RemuneracionResponse(RemuneracionBase):
    id: int
    empleado_id: int
    
    class Config:
        from_attributes = True


class DescuentoBase(BaseModel):
    periodo: str
    afp_aporte: Decimal = Decimal("0.00")
    afp_prima: Decimal = Decimal("0.00")
    afp_seguro: Decimal = Decimal("0.00")
    onp: Decimal = Decimal("0.00")
    faltas: int = 0
    tardanzas: Decimal = Decimal("0.00")
    anticipos: Decimal = Decimal("0.00")
    otros: Decimal = Decimal("0.00")
    total_descuento: Decimal = Decimal("0.00")


class DescuentoCreate(DescuentoBase):
    empleado_id: int


class DescuentoResponse(DescuentoBase):
    id: int
    empleado_id: int
    
    class Config:
        from_attributes = True


class BeneficioSocialBase(BaseModel):
    tipo: str
    periodo: str
    tiempo: Decimal
    basico: Decimal
    promedio: Decimal
    monto: Decimal
    fecha_pago: Optional[date] = None
    estado: str = "pendiente"


class BeneficioSocialCreate(BeneficioSocialBase):
    empleado_id: int


class BeneficioSocialResponse(BeneficioSocialBase):
    id: int
    empleado_id: int
    
    class Config:
        from_attributes = True


class AsistenciaBase(BaseModel):
    fecha: date
    hora_entrada: Optional[date] = None
    hora_salida: Optional[date] = None
    hora_entrada_min: Optional[date] = None
    horas_trabajadas: Decimal = Decimal("0.00")
    horas_extras: Decimal = Decimal("0.00")
    falta: bool = False
    permiso: str = ""
    observacion: str = ""


class AsistenciaCreate(AsistenciaBase):
    empresa_id: int
    empleado_id: int


class AsistenciaResponse(AsistenciaBase):
    id: int
    empresa_id: int
    empleado_id: int
    
    class Config:
        from_attributes = True


class PlanillaBase(BaseModel):
    periodo: str
    total_empleados: int = 0
    total_ingresos: Decimal = Decimal("0.00")
    total_descuentos: Decimal = Decimal("0.00")
    total_aportes: Decimal = Decimal("0.00")
    total_neto: Decimal = Decimal("0.00")
    estado: str = "borrador"


class PlanillaCreate(PlanillaBase):
    empresa_id: int


class PlanillaResponse(PlanillaBase):
    id: int
    empresa_id: int
    archivo_plame: Optional[str] = None
    archivo_pdf: Optional[str] = None
    fecha_cierre: Optional[date] = None
    fecha_registro: datetime
    
    class Config:
        from_attributes = True