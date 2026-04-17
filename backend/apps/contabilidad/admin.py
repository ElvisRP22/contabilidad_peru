from django.contrib import admin
from .models import PlanCuenta, Asiento, DetalleAsiento, CentroCosto


@admin.register(PlanCuenta)
class PlanCuentaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'naturaleza', 'tipo_cuenta', 'nivel', 'acepta_movimiento']
    list_filter = ['naturaleza', 'tipo_cuenta', 'nivel']
    search_fields = ['codigo', 'nombre']
    raw_id_fields = ['padre']


class DetalleAsientoInline(admin.TabularInline):
    model = DetalleAsiento
    extra = 1
    fields = ['cuenta', 'debe', 'haber', 'glosa']


@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'fecha', 'debe', 'haber', 'estado', 'cerrado']
    list_filter = ['estado', 'cerrado', 'fecha']
    search_fields = ['numero', 'glosa']
    inlines = [DetalleAsientoInline]
    raw_id_fields = ['usuario_registra', 'usuario_aprueba']


@admin.register(CentroCosto)
class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']