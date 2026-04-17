from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class PlanCuenta(models.Model):
    NATURALEZA_CHOICES = [
        ('deudora', 'Deudora'),
        ('acreedora', 'Acreedora'),
    ]
    
    TIPO_CUENTA_CHOICES = [
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('patrimonio', 'Patrimonio'),
        ('resultado_deudor', 'Resultado Deudor'),
        ('resultado_acreedor', 'Resultado Acreedor'),
    ]
    
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='plan_cuentas')
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=200)
    naturaleza = models.CharField(max_length=10, choices=NATURALEZA_CHOICES)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES)
    nivel = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='hijos')
acepta_movimiento = models.BooleanField(default=True)
    cta_banco = models.BooleanField(default=False)
    cta_efectivo = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'contabilidad_plan_cuenta'
        verbose_name = 'Plan de Cuenta'
        verbose_name_plural = 'Plan de Cuentas'
        unique_together = ['empresa', 'codigo']
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def tiene_hijos(self):
        return self.hijos.exists()


class Asiento(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='asientos')
    numero = models.CharField(max_length=20)
    fecha = models.DateField()
    glosa = models.TextField(blank=True)
    debe = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    haber = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    estado = models.CharField(max_length=20, default='pendiente')
    cerrado = models.BooleanField(default=False)
    usuario_registra = models.ForeignKey('core.Usuario', on_delete=models.SET_NULL, null=True, related_name='asientos_registrados')
    usuario_aprueba = models.ForeignKey('core.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='asientos_aprobados')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_aprueba = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'contabilidad_asiento'
        verbose_name = 'Asiento'
        verbose_name_plural = 'Asientos'
        ordering = ['-fecha', '-numero']
    
    def __str__(self):
        return f"Asiento {self.numero} - {self.fecha}"
    
    def calcular_totales(self):
        from django.db.models import Sum
        totales = self.detalles.aggregate(
            total_debe=Sum('debe'),
            total_haber=Sum('haber')
        )
        self.debe = totales['total_debe'] or Decimal('0.00')
        self.haber = totales['total_haber'] or Decimal('0.00')
        return self.debe == self.haber
    
    def validar_partida_doble(self):
        return self.calcular_totales()


class DetalleAsiento(models.Model):
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name='detalles')
    cuenta = models.ForeignKey(PlanCuenta, on_delete=models.PROTECT, related_name='movimientos')
    debe = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    haber = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
   glosa = models.TextField(blank=True)
    centro_costo = models.ForeignKey('CentroCosto', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'contabilidad_detalle_asiento'
        verbose_name = 'Detalle de Asiento'
        verbose_name_plural = 'Detalles de Asientos'
    
    def __str__(self):
        return f"{self.cuenta.codigo} - Debe:{self.debe} Haber:{self.haber}"


class CentroCosto(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='centros_costo')
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'contabilidad_centro_costo'
        verbose_name = 'Centro de Costo'
        verbose_name_plural = 'Centros de Costo'
        unique_together = ['empresa', 'codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"