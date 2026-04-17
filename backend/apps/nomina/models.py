from django.db import models
from decimal import Decimal


class Empleado(models.Model):
    TIPO_DOC_CHOICES = [
        ('1', 'DNI'),
        ('4', 'Carnet de Extranjería'),
        ('6', 'RUC'),
        ('7', 'Pasaporte'),
    ]
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='empleados')
    numero_documento = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOC_CHOICES, default='1')
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    direccion = models.CharField(max_length=300, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    fecha_ingreso = models.DateField()
    fecha_cese = models.DateField(null=True, blank=True)
    motivo_cese = models.CharField(max_length=200, blank=True)
    
    cargo = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    
    regimen_laboral = models.CharField(max_length=50, default='General')
    jornada_trabajo = models.IntegerField(default=8, help_text='Horas por día')
    
    tipo_contrato = models.CharField(max_length=50, default='Indeterminado')
    syndicate = models.BooleanField(default=False)
    
    cuenta_banco = models.CharField(max_length=30, blank=True)
    banco = models.CharField(max_length=50, blank=True)
    
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'nomina_empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        unique_together = ['empresa', 'numero_documento']
        ordering = ['apellido_paterno', 'apellido_materno', 'nombres']
    
    def __str__(self):
        return f"{self.numero_documento} - {self.apellido_paterno} {self.apellido_materno}, {self.nombres}"
    
    def get_full_name(self):
        return f"{self.apellido_paterno} {self.apellido_materno}, {self.nombres}"


class Remuneracion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='remuneraciones')
    periodo = models.CharField(max_length=7)  # YYYY-MM
    
    basic_salary = models.DecimalField(max_digits=15, decimal_places=2)
    asig_familiar = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    bonificacion = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
   comision = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    overtime = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    otros = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    ingreso_gravado = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    ingreso_no_gravado = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_ingreso = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        db_table = 'nomina_remuneracion'
        verbose_name = 'Remuneración'
        verbose_name_plural = 'Remuneraciones'
        unique_together = ['empleado', 'periodo']


class Descuento(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='descuentos')
    periodo = models.CharField(max_length=7)
    
    afp_aporte = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    afp_prima = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    afp_seguro = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    onp = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    faltas = models.IntegerField(default=0)
    tardanzas = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    anticipos = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    otros = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    total_descuento = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        db_table = 'nomina_descuento'
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        unique_together = ['empleado', 'periodo']


class BeneficioSocial(models.Model):
    TIPO_CHOICES = [
        ('cts', 'CTS'),
        ('gratificacion', 'Gratificación'),
        ('utilidades', 'Utilidades'),
        ('liquidacion', 'Liquidación'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='beneficios')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    periodo = models.CharField(max_length=10)
    
    tiempo = models.DecimalField(max_digits=5, decimal_places=2, help_text='Meses trabajados')
    basico = models.DecimalField(max_digits=15, decimal_places=2)
    promedio = models.DecimalField(max_digits=15, decimal_places=2)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    
    fecha_pago = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='pendiente')
    
    class Meta:
        db_table = 'nomina_beneficio'
        verbose_name = 'Beneficio Social'
        verbose_name_plural = 'Beneficios Sociales'
        unique_together = ['empleado', 'tipo', 'periodo']


class Asistencia(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='asistencias')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    hora_entrada_min = models.TimeField(null=True, blank=True)
    
    horas_trabajadas = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    horas_extras = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    
    falta = models.BooleanField(default=False)
    permiso = models.CharField(max_length=200, blank=True)
    observacion = models.TextField(blank=True)
    
    class Meta:
        db_table = 'nomina_asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ['empleado', 'fecha']


class Planilla(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='planillas')
    periodo = models.CharField(max_length=7)
    
    total_empleados = models.IntegerField(default=0)
    total_ingresos = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_descuentos = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_aportes = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_neto = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    archivo_plame = models.FileField(upload_to='planillas/', null=True, blank=True)
    archivo_pdf = models.FileField(upload_to='planillas/', null=True, blank=True)
    
    estado = models.CharField(max_length=20, default='borrador')
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'nomina_planilla'
        verbose_name = 'Planilla'
        verbose_name_plural = 'Planillas'
        unique_together = ['empresa', 'periodo']
        ordering = ['-periodo']