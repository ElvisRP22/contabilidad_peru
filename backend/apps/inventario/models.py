from django.db import models
from decimal import Decimal


class Almacen(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='almacenes')
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True)
    principal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventario_almacen'
        verbose_name = 'Almacén'
        verbose_name_plural = 'Almacenes'
        unique_together = ['empresa', 'codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Categoria(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='categorias')
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')
    
    class Meta:
        db_table = 'inventario_categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        unique_together = ['empresa', 'codigo']
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Producto(models.Model):
    UNIDAD_CHOICES = [
        ('NIU', 'Unidad'),
        ('KGM', 'Kilogramo'),
        ('LTR', 'Litro'),
        ('PZA', 'Pieza'),
        ('CJA', 'Caja'),
    ]
    
    METODO_VALORACION_CHOICES = [
        ('promedio', 'Promedio Ponderado'),
        ('fifo', 'PEPS/Primero entradas, primeras salidas'),
        ('lifo', 'LIFO/Últimas entradas, primeras salidas'),
    ]
    
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='productos')
    codigo = models.CharField(max_length=30, db_index=True)
    codigo_barras = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    unidad = models.CharField(max_length=3, choices=UNIDAD_CHOICES, default='NIU')
    presentacion = models.CharField(max_length=50, blank=True)
    
    cantidad = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0.000'))
    cantidad_minima = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0.000'))
    cantidad_maxima = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0.000'))
    
    costo_unitario = models.DecimalField(max_digits=15, decimal_places=10, default=Decimal('0.0000000000'))
    precio_venta = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    permite_stock_negativo = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    afecta_igv = models.BooleanField(default=True)
    tipo_afectacion = models.CharField(max_length=2, default='10')
    
    class Meta:
        db_table = 'inventario_producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        unique_together = ['empresa', 'codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Kardex(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste_positivo', 'Ajuste Positivo'),
        ('ajuste_negativo', 'Ajuste Negativo'),
    ]
    
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='kardex')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='kardex')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='kardex')
    
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    numero_documento = models.CharField(max_length=20, blank=True)
    fecha_movimiento = models.DateField()
    
    cantidad = models.DecimalField(max_digits=15, decimal_places=3)
    costo_unitario = models.DecimalField(max_digits=15, decimal_places=10)
    costo_total = models.DecimalField(max_digits=15, decimal_places=2)
    
    cantidad_saldo = models.DecimalField(max_digits=15, decimal_places=3)
    costo_promedio = models.DecimalField(max_digits=15, decimal_places=10)
    costo_saldo = models.DecimalField(max_digits=15, decimal_places=2)
    
    glosa = models.TextField(blank=True)
    referencia_id = models.PositiveIntegerField(null=True, blank=True)
    referencia_tipo = models.CharField(max_length=20, blank=True)
    
    usuario_registra = models.ForeignKey('core.Usuario', on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inventario_kardex'
        verbose_name = 'Kárdex'
        verbose_name_plural = 'Kárdex'
        ordering = ['-fecha_movimiento', '-id']
    
    def __str__(self):
        return f"{self.producto.codigo} - {self.fecha_movimiento}"


class StockAlmacen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='stocks')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='stocks')
    cantidad = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0.000'))
    costo_promedio = models.DecimalField(max_digits=15, decimal_places=10, default=Decimal('0.0000000000'))
    
    class Meta:
        db_table = 'inventario_stock_almacen'
        verbose_name = 'Stock por Almacén'
        verbose_name_plural = 'Stocks por Almacén'
        unique_together = ['producto', 'almacen']
    
    def __str__(self):
        return f"{self.producto.codigo} - {self.almacen.codigo}: {self.cantidad}"