from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Comprobante(models.Model):
    TIPO_DOC_CHOICES = [
        ('01', 'Factura'),
        ('03', 'Boleta'),
        ('07', 'Nota de Crédito'),
        ('08', 'Nota de Débito'),
    ]
    
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('generado', 'Generado'),
        ('firmado', 'Firmado'),
        ('enviado', 'Enviado'),
        ('aceptado', 'Aceptado'),
        ('observado', 'Observado'),
        ('rechazado', 'Rechazado'),
        ('anulado', 'Anulado'),
    ]
    
    moneda = models.CharField(max_length=3, default='PEN')
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('1.000'))
    fecha_emision = models.DateField()
    hora_emision = models.TimeField(null=True, blank=True)
    
    serie = models.CharField(max_length=4)
    correlativo = models.CharField(max_length=8)
    numero = models.CharField(max_length=13, unique=True)
    
    cliente_tipo_documento = models.CharField(max_length=2)
    cliente_numero_documento = models.CharField(max_length=20)
    cliente_denominacion = models.CharField(max_length=200)
    cliente_direccion = models.TextField(blank=True)
    
    importe_subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    importe_igv = models.DecimalField(max_digits=15, decimal_places=2)
    importe_total = models.DecimalField(max_digits=15, decimal_places=2)
    
    formato = models.CharField(max_length=10, default='json')
    observaciones = models.TextField(blank=True)
    
    xml_firmado = models.TextField(blank=True)
    hash_cpe = models.CharField(max_length=100, blank=True)
   cdr_sunat = models.TextField(blank=True)
    codigo_respuesta = models.CharField(max_length=10, blank=True)
    descripcion_respuesta = models.TextField(blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    pdf_url = models.URLField(blank=True)
    xml_url = models.URLField(blank=True)
    cdr_url = models.URLField(blank=True)
    
    referencia_documento = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='notas')
    referencia_motivo = models.CharField(max_length=100, blank=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facturacion_comprobante'
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'
        ordering = ['-fecha_emision', '-correlativo']
    
    def __str__(self):
        return self.numero
    
    def generar_numero(self):
        return f"{self.serie}-{self.correlativo.zfill(8)}"


class DetalleComprobante(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, related_name='detalles')
    numero_item = models.IntegerField(validators=[MinValueValidator(1)])
    
    codigo_producto = models.CharField(max_length=30, blank=True)
    descripcion = models.TextField()
    
    unidad = models.CharField(max_length=3, default='NIU')
    cantidad = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('1.000'))
    
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=10)
    precio_base = models.DecimalField(max_digits=15, decimal_places=2)
    
    tipo_afectacion_igv = models.CharField(max_length=2, default='10')
    porcentaje_igv = models.CharField(max_length=5, default='18')
    igv = models.DecimalField(max_digits=15, decimal_places=2)
    
    monto_descuento = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    importe_total = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        db_table = 'facturacion_detalle_comprobante'
        verbose_name = 'Detalle de Comprobante'
        verbose_name_plural = 'Detalles de Comprobantes'
        unique_together = ['comprobante', 'numero_item']


class DocumentoReferencia(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, related_name='referencias')
    tipo_documento = models.CharField(max_length=2)
    serie = models.CharField(max_length=4)
    correlativo = models.CharField(max_length=8)
    motivo = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'facturacion_documento_referencia'
        verbose_name = 'Documento de Referencia'


class HistorialEnvio(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, related_name='historial_envios')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20)
    request_data = models.TextField(blank=True)
    response_data = models.TextField(blank=True)
    estado = models.CharField(max_length=20)
    mensaje = models.TextField(blank=True)
    
    class Meta:
        db_table = 'facturacion_historial_envio'
        verbose_name = 'Historial de Envío'
        verbose_name_plural = 'Historiales de Envío'