from django.contrib import admin
from .models import Empleado, Remuneracion, Descuento, BeneficioSocial, Asistencia, Planilla


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'apellido_paterno', 'apellido_materno', 'nombres', 'cargo', 'activo']
    list_filter = ['activo', 'area', 'regimen_laboral']
    search_fields = ['numero_documento', 'nombres', 'apellido_paterno']


@admin.register(Remuneracion)
class RemuneracionAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'periodo', 'basic_salary', 'total_ingreso']
    list_filter = ['periodo']
    raw_id_fields = ['empleado']


@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'periodo', 'total_descuento']
    list_filter = ['periodo']
    raw_id_fields = ['empleado']


@admin.register(BeneficioSocial)
class BeneficioSocialAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'tipo', 'periodo', 'monto', 'estado']
    list_filter = ['tipo', 'estado', 'periodo']
    raw_id_fields = ['empleado']


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'fecha', 'hora_entrada', 'hora_salida', 'falta']
    list_filter = ['fecha', 'falta']
    raw_id_fields = ['empleado']


@admin.register(Planilla)
class PlanillaAdmin(admin.ModelAdmin):
    list_display = ['periodo', 'total_empleados', 'total_ingresos', 'total_neto', 'estado']
    list_filter = ['periodo', 'estado']