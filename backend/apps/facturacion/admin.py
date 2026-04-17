from django.contrib import admin
from .models import Comprobante, DetalleComprobante, DocumentoReferencia, HistorialEnvio


class DetalleComprobanteInline(admin.TabularInline):
    model = DetalleComprobante
    extra = 1
    fields = ['numero_item', 'codigo_producto', 'descripcion', 'unidad', 'cantidad', 
             'precio_unitario', 'precio_base', 'tipo_afectacion_igv', 'igv', 'importe_total']


@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo_documento', 'cliente_denominacion', 'importe_total', 'estado', 'fecha_emision']
    list_filter = ['tipo_documento', 'estado', 'fecha_emision']
    search_fields = ['numero', 'cliente_denominacion', 'cliente_numero_documento']
    inlines = [DetalleComprobanteInline]
    raw_id_fields = ['referencia_documento']


@admin.register(HistorialEnvio)
class HistorialEnvioAdmin(admin.ModelAdmin):
    list_display = ['comprobante', 'fecha_envio', 'tipo', 'estado']
    list_filter = ['tipo', 'estado']