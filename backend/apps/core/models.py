from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('contador', 'Contador'),
        ('cliente', 'Cliente'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='cliente')
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'core_usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.get_full_name() or self.username


class Empresa(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('ruc', 'RUC'),
        ('dni', 'DNI'),
        ('ce', 'Carnet de Extranjería'),
    ]
    
    TIPO_REGIMEN_CHOICES = [
        ('general', 'Régimen General'),
        ('mype', 'Régimen MYPE'),
        ('agricola', 'Agrario'),
        (' Construccion', 'Construcción Civil'),
    ]
    
    razon_social = models.CharField(max_length=200)
    nombre_comercial = models.CharField(max_length=200, blank=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES, default='ruc')
    numero_documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=300, blank=True)
    departamento = models.CharField(max_length=50, blank=True)
    provincia = models.CharField(max_length=50, blank=True)
    distrito = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    tipo_regimen = models.CharField(max_length=20, choices=TIPO_REGIMEN_CHOICES, default='general')
    representante_legal = models.CharField(max_length=200, blank=True)
    dni_representante = models.CharField(max_length=20, blank=True)
    
    certificado_digital = models.FileField(upload_to='certificados/', null=True, blank=True)
    password_certificado = models.CharField(max_length=100, blank=True)
    
    ose_enabled = models.BooleanField(default=False)
    ose_proveedor = models.CharField(max_length=100, blank=True)
    ose_token = models.CharField(max_length=200, blank=True)
    
    activa = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['razon_social']
    
    def __str__(self):
        return f"{self.numero_documento} - {self.razon_social}"


class SerieDocumento(models.Model):
    TIPO_DOC_CHOICES = [
        ('01', 'Factura'),
        ('03', 'Boleta'),
        ('07', 'Nota de Crédito'),
        ('08', 'Nota de Débito'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='series')
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOC_CHOICES)
    serie = models.CharField(max_length=4)
    correlativo = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        db_table = 'core_serie_documento'
        verbose_name = 'Serie de Documento'
        verbose_name_plural = 'Series de Documentos'
        unique_together = ['empresa', 'tipo_documento', 'serie']
    
    def __str__(self):
        return f"{self.tipo_documento}-{self.serie}"


class ParametroSistema(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='parametros')
    clave = models.CharField(max_length=50)
    valor = models.TextField()
    descripcion = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'core_parametro'
        verbose_name = 'Parámetro'
        verbose_name_plural = 'Parámetros'
        unique_together = ['empresa', 'clave']
    
    def __str__(self):
        return f"{self.empresa}-{self.clave}"