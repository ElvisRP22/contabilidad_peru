from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship


class Empleado(SQLModel, table=True):
    __tablename__ = "nomina_empleado"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    numero_documento: str = Field(max_length=20)
    tipo_documento: str = Field(default="1")
    nombres: str = Field(max_length=100)
    apellido_paterno: str = Field(max_length=50)
    apellido_materno: str = Field(max_length=50)
    sexo: str
    fecha_nacimiento: Optional[date] = None
    
    direccion: str = Field(default="")
    telefono: str = Field(default="")
    email: Optional[str] = None
    
    fecha_ingreso: date
    fecha_cese: Optional[date] = None
    motivo_cese: str = Field(default="")
    
    cargo: str = Field(default="")
    area: str = Field(default="")
    
    regimen_laboral: str = Field(default="General")
    jornada_trabajo: int = Field(default=8)
    tipo_contrato: str = Field(default="Indeterminado")
    sindicate: bool = Field(default=False)
    
    cuenta_banco: str = Field(default="")
    banco: str = Field(default="")
    
    activo: bool = Field(default=True)
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    
    def get_full_name(self) -> str:
        return f"{self.apellido_paterno} {self.apellido_materno}, {self.nombres}"


class Remuneracion(SQLModel, table=True):
    __tablename__ = "nomina_remuneracion"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empleado_id: int = Field(foreign_key="nomina_empleado.id")
    periodo: str = Field(max_length=7)
    
    basic_salary: Decimal = Field(decimal_places=2, max_digits=15)
    asig_familiar: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    bonificacion: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    comision: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    overtime: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    otros: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    
    ingreso_gravado: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    ingreso_no_gravado: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    total_ingreso: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)


class Descuento(SQLModel, table=True):
    __tablename__ = "nomina_descuento"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empleado_id: int = Field(foreign_key="nomina_empleado.id")
    periodo: str = Field(max_length=7)
    
    afp_aporte: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    afp_prima: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    afp_seguro: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    onp: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    
    faltas: int = Field(default=0)
    tardanzas: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=5)
    anticipos: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    otros: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    
    total_descuento: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)


class BeneficioSocial(SQLModel, table=True):
    __tablename__ = "nomina_beneficio"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empleado_id: int = Field(foreign_key="nomina_empleado.id")
    tipo: str
    periodo: str = Field(max_length=10)
    
    tiempo: Decimal = Field(decimal_places=2, max_digits=5)
    basico: Decimal = Field(decimal_places=2, max_digits=15)
    promedio: Decimal = Field(decimal_places=2, max_digits=15)
    monto: Decimal = Field(decimal_places=2, max_digits=15)
    
    fecha_pago: Optional[date] = None
    estado: str = Field(default="pendiente")


class Asistencia(SQLModel, table=True):
    __tablename__ = "nomina_asistencia"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    empleado_id: int = Field(foreign_key="nomina_empleado.id")
    fecha: date
    
    hora_entrada: Optional[date] = None
    hora_salida: Optional[date] = None
    hora_entrada_min: Optional[date] = None
    
    horas_trabajadas: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=5)
    horas_extras: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=5)
    
    falta: bool = Field(default=False)
    permiso: str = Field(default="")
    observacion: str = Field(default="")


class Planilla(SQLModel, table=True):
    __tablename__ = "nomina_planilla"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="core_empresa.id")
    periodo: str = Field(max_length=7)
    
    total_empleados: int = Field(default=0)
    total_ingresos: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    total_descuentos: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    total_aportes: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    total_neto: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    
    archivo_plame: Optional[str] = None
    archivo_pdf: Optional[str] = None
    
    estado: str = Field(default="borrador")
    fecha_cierre: Optional[date] = None
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)