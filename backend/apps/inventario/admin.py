from django.contrib import admin
from .models import Almacen, Categoria, Producto, Kardex, StockAlmacen


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'principal', 'activo']
    list_filter = ['principal', 'activo']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'padre']
    list_filter = ['padre']
    search_fields = ['codigo', 'nombre']


class KardexInline(admin.TabularInline):
    model = Kardex
    extra = 0
    readonly_fields = ['producto', 'tipo_movimiento', 'cantidad', 'costo_unitario', 'cantidad_saldo']
    can_delete = False


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'cantidad', 'costo_unitario', 'precio_venta', 'activo']
    list_filter = ['categoria', 'activo', 'afecta_igv']
    search_fields = ['codigo', 'nombre', 'codigo_barras']
    raw_id_fields = ['categoria']


@admin.register(Kardex)
class KardexAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo_movimiento', 'cantidad', 'costo_unitario', 'fecha_movimiento']
    list_filter = ['tipo_movimiento', 'fecha_movimiento']
    search_fields = ['numero_documento', 'producto__nombre']
    raw_id_fields = ['producto', 'almacen', 'usuario_registra']


@admin.register(StockAlmacen)
class StockAlmacenAdmin(admin.ModelAdmin):
    list_display = ['producto', 'almacen', 'cantidad', 'costo_promedio']
    raw_id_fields = ['producto', 'almacen']